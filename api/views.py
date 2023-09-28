from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import openpyxl
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Sum, Count


from api.models import Project, Excel, Province, District, Municipality
from api.serializers import ProjectSerializer, ExcelSerializer, SummarySerializer, SecondSummarySerializer, ProvinceSerializer, DistrictSerializer, MunicipalitySerializer
from api.fieldmapper import field_map, province_mapper

from api.enums import province_choices
from api.municipality import  list_of_district, municipality_detail, district_isto_municipality

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "sector", "province", "agreement_date"]

    filter_backends.append(SearchFilter)
    search_fields = ["title"]


    @action(detail=False, methods=["get"])
    def sector_summary(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        project_count = queryset.count()
        total_budget = queryset.aggregate(result=Sum("commitments")).get("result")
        sector_summary = queryset.values("sector").annotate(
            project_count=Count("sector"),
            budget=Sum("commitments"),
        )
        for i in sector_summary:
            i['name'] = i.pop('sector') 
        serializer = SummarySerializer(sector_summary, many=True)
        summary_data = {
            "project_count": project_count,
            "total_budget": total_budget,
            "sector": serializer.data,
        }
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def status_summary(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        project_count = queryset.count()
        total_budget = queryset.aggregate(result=Sum("commitments"))["result"]

        status_summary = queryset.values("status").annotate(
            project_count=Count("status"),
            budget=Sum("commitments"),
        )
        for i in status_summary:
            i['name'] = i.pop('status')

        serializer = SummarySerializer(status_summary, many=True)
        summary_data = {
            "project_count": project_count,
            "total_budget": total_budget,
            "status": serializer.data,
        }
        return Response(summary_data)

    @action(detail=False, methods=["get"])
    def province_summary(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        project_count = queryset.count()
        total_budget = queryset.aggregate(result=Sum("commitments"))["result"]

        province_summary = queryset.values("province").annotate(
            project_count=Count("province"),
            budget=Sum("commitments"),
        )
        for i in province_summary:
            i['name'] = i.pop('province')

        serializer = SummarySerializer(province_summary, many=True)
        summary_data = {
            "project_count": project_count,
            "total_budget": total_budget,
            "province": serializer.data,
        }
        return Response(summary_data)

    @action(detail=False, methods=["get"])
    def agreement_date_summary(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        project_count = queryset.count()
        total_budget = queryset.aggregate(result=Sum("commitments"))["result"]
        agreement_date_summary = queryset.values("agreement_date").annotate(
            project_count=Count("agreement_date"),
            budget=Sum("commitments"),
        )
        for i in agreement_date_summary:
            i['name'] = i.pop('agreement_date')

        serializer = SummarySerializer(agreement_date_summary, many=True)
        summary_data = {
            "project_count": project_count,
            "total_budget": total_budget,
            "aggrement_date": serializer.data,
        }
        return Response(summary_data)
    
    @action(detail=False, methods=['get'])
    def municipality_summary(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        municipality_summary = queryset.values('municipality').annotate(
            count = Count('municipality'),
            budget = Sum('commitments'),
        )
        for i in municipality_summary:
            i['name'] = i.pop('municipality')
        serializer = SecondSummarySerializer(municipality_summary, many = True)
        return Response(serializer.data)        

    @action(detail=False, methods=['get'])
    def district_summary(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        district_summary = queryset.values('district').annotate(
            count = Count('district'),
            budget = Sum('commitments'),
        )
        for i in district_summary:
            i['name'] = i.pop('district')
        serializer = SecondSummarySerializer(district_summary, many = True)
        return Response(serializer.data)     


class ExcelViewSet(ModelViewSet):
    queryset = Excel.objects.all()
    serializer_class = ExcelSerializer

    def create(self, request, *args, **kwargs):
        """
        This will post the excel data to the Project Model.
        """
        excel_serializer = ExcelSerializer(data=request.data)
        if excel_serializer.is_valid():
            excel_file = excel_serializer.validated_data["excel_file"]
            workbook = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = workbook.active
            headers = [cell.value for cell in sheet[1] if cell.column != "O"]
            list_of_dictionary = []

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if any(cell is None for cell in row):
                    continue
                each_row_values = {}
                for header, value in zip(headers, row):
                    if header in field_map:
                        field_name = field_map[header]
                        if value is not None and header != "O":
                            each_row_values[field_name] = value
                list_of_dictionary.append(each_row_values)

            for data in list_of_dictionary:
                province = province_mapper.get(data.get('province'))
                province_obj, created = Province.objects.get_or_create(name = province)
                data['province'] = province_obj
                district = data.get('district')
                district_obj, created = District.objects.get_or_create(name = district)
                data['district'] = district_obj
                municipality = data.get('municipality')
                municipality_obj, created = Municipality.objects.get_or_create(name = municipality, district = district_obj, province = province_obj)
                data['municipality'] = municipality_obj

            # for data in list_of_dictionary:
            #     Project.objects.create(**data)

            Project.objects.bulk_create(
                [Project(**data) for data in list_of_dictionary]
            )
            return Response(
                {"message": "Data from Excel file has been imported."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(excel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProvinceViewSet(ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    
    @action(detail=False,url_path='populate-provinces')
    def populate_provinces(self,request, *args, **kwargs):
        # for key,value in province_mapper.items():
        #     province_obj,created = Province.objects.create(code = key, name = value)
                                               
        for code, name in province_choices:
            province_obj, created = Province.objects.get_or_create(code = code, name = name)
        return Response({'msg':'Province populated successfully.'})
            

class DistrictViewSet(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    @action(detail=False, url_path='populate_districts')
    def populate_districts(self, request, *args, **kwargs):
        # for key, value in district_isto_municipality.items():
        #     district,created = District.objects.get_or_create(name = key, municipalities = value)

        for key in list_of_district:
            district,created = District.objects.get_or_create(name = key)
        return Response({'msg':'Districts created successfully.'})


class MunicipalityViewSet(ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer

    @action(detail= False,url_path='populate_municipality')
    def populate_municipality(self, request, *args, **kwargs):
    
        for detail in municipality_detail:
            name = detail.get('name')

            dname = detail.get('district')
            district,_ = District.objects.get_or_create(name = dname)
            district_name  = district.name

            pname = detail.get('province')
            province,_ = Province.objects.get_or_create(name = pname)
            province_name = province.name

            country = detail.get('country') 
            municipality_obj, created = Municipality.objects.get_or_create(name = name , district = district, province = province)
        return Response(
            {
                'msg':'Municipality created successfully.'
            }
        )
