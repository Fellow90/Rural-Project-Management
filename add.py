from nepali_municipalities import NepalMunicipality
nepal_municipality = NepalMunicipality()
list_of_district = nepal_municipality.all_districts()

district_isto_municipality = {}
list_of_municipalities = []
municipality_detail = []

for i in list_of_district:
    municipalities_list = NepalMunicipality(district_name=i).all_municipalities()
    district_isto_municipality[i] = municipalities_list

    for j in municipalities_list:
        municipalities = {}
        municipality_wise_detail =  NepalMunicipality().all_data_info(municipality_name=j)
        # print(municipality_wise_detail)

        for k in municipality_wise_detail:
            municipality_detail.append(k)

            if k['district'] == i:
                municipalities[j] = k
                list_of_municipalities.append(municipalities)

##municipality detail provides the list of municipality in detail
##list of municipality provides the list of municipality with key as municipality name
##list of districts provide the list of districts 
##municipality isto detail provides detail of municipality with respect to key

print(municipality_detail)