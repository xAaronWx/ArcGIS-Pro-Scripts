# -*- coding: UTF-8 -*-
"""
   Copyright 2020 Aaron J White
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.​
    This sample adds and updates Wet Weather Inspection metadata fields in a feature class.
"""
import arcpy
import argparse
import os


def get_geodatabase_path(input_layer):
    """
    Gets the parent geodatabase of the layer
    :param input_layer: (string) The feature layer to get the parent database of
    :return: (string) The path to the geodatabase
    """
    workspace = os.path.dirname(arcpy.Describe(input_layer).catalogPath)
    if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
        return workspace
    else:
        return os.path.dirname(workspace)


def check_and_create_domains(geodatabase):
    """
    Checks if the domains already exist, if they do
    then it checks the values and ranges

    If the domains do not exist, they are created

    :param geodatabase: (string) the path to the geodatabase to check
    :return:
    """
    domains = arcpy.da.ListDomains(geodatabase)
    domain_names = [domain.name for domain in domains]
    if 'Yes_No' in domain_names:
        for domain in domains:
            if domain.name == 'Yes_No':
                # check if cvs 0,1,2,4,5 are in the codedValues
                values = [cv for cv in domain.codedValues]
                if not set(set([0, 1, 2, 4, 5])).issubset(values):
                    arcpy.AddIDMessage("ERROR This domain already exists")
                    return
    else:
        # Add the domain and values
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="Yes_No",
                                      domain_description="Yes or No",
                                      field_type="TEXT",
                                      domain_type="CODED",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")

        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="Yes_No",
                                               code="Yes",
                                               code_description="Yes")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="Yes_No",
                                               code="No",
                                               code_description="No")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="Yes_No",
                                               code="N/A",
                                               code_description="N/A")

    # Check if 'Inspector" is a domain, if so check the range
    if 'Inspector' in domain_names:
        for domain in domains:
            if domain.name == 'Inspector':
                # check if cvs 0,1,2,4,5 are in the codedValues
                values = [cv for cv in domain.codedValues]
                if not set(set([0, 1, 2, 4, 5])).issubset(values):
                    arcpy.AddIDMessage("ERROR This domain already exists")
                    return
    else:
        # Add the domain and set the range
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="Inspector",
                                      domain_description="Inspector",
                                      field_type="TEXT",
                                      domain_type="CODED",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")

    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="ALA",
                                           code_description="ALA")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="BAR",
                                           code_description="BAR")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="BUR",
                                           code_description="BUR")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="CAS",
                                           code_description="CAS")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="JJH",
                                           code_description="JJH")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="JLK",
                                           code_description="JLK")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="JWN",
                                           code_description="JWN")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="MJT",
                                           code_description="MJT")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="REM",
                                           code_description="REM")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="RWG",
                                           code_description="RWG")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="SAB",
                                           code_description="SAB")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="SJS",
                                           code_description="SJS")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="SUB",
                                           code_description="SUB")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Inspector",
                                           code="WBH",
                                           code_description="WBH")


#  Check if Flow Percentage is a domain
    if 'Flow_Percent' in domain_names:
        for domain in domains:
            if domain.name == 'Flow_Percent':
                # check if cvs 0,1,2,4,5 are in the codedValues
                values = [cv for cv in domain.codedValues]
                if not set(set([0, 1, 2, 4, 5])).issubset(values):
                    arcpy.AddIDMessage("ERROR This domain already exists")
                    return
    else:
        # Add the domain and set the range
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="Flow_Percent",
                                      domain_description="Flow Percentage",
                                      field_type="TEXT",
                                      domain_type="CODED",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")

    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Flow_Percent",
                                           code="0",
                                           code_description="0% (No Flow)")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Flow_Percent",
                                           code="25",
                                           code_description="25%")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Flow_Percent",
                                           code="50",
                                           code_description="50%")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Flow_Percent",
                                           code="75",
                                           code_description="75%")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Flow_Percent",
                                           code="100",
                                           code_description="100%")

#  Check if Clock Position is a domain
    if 'Clock_Pos' in domain_names:
        for domain in domains:
            if domain.name == 'Clock_Pos':
                # check if cvs 0,1,2,4,5 are in the codedValues
                values = [cv for cv in domain.codedValues]
                if not set(set([0, 1, 2, 4, 5])).issubset(values):
                    arcpy.AddIDMessage("ERROR This domain already exists")
                    return
    else:
        # Add the domain and set the range
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="Clock_Pos",
                                      domain_description="Clock Position",
                                      field_type="TEXT",
                                      domain_type="CODED",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")

    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="1",
                                           code_description="1 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="10",
                                           code_description="10 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="11",
                                           code_description="11 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="12",
                                           code_description="12 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="2",
                                           code_description="2 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="3",
                                           code_description="3 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="4",
                                           code_description="4 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="5",
                                           code_description="5 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="6",
                                           code_description="6 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="7",
                                           code_description="7 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="8",
                                           code_description="8 o'clock")
    arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                           domain_name="Clock_Pos",
                                           code="9",
                                           code_description="9 o'clock")


def wet_weather(feature_layer):
    """
    This adds specific fields required for wet weather inspections

        This will report errors if:
            1) Any of the fields already exist
            2) The input layer is not a point layer
            3) The layer is not found
            4) The layer is a shapefile

    Example: add_gps_fields(r"C:/temp/test.shp")

    :param feature_layer: (string) The feature layer (shapefile, feature class, etc) to add the fields to
    :return:
    """

    try:
       # need to know dataType of input
        desc = arcpy.Describe(feature_layer)
        dataType = desc.dataType.lower()
        if dataType == "featurelayer":
            dataType = arcpy.Describe(
                feature_layer).dataElement.dataType.lower()

        # catch invalid inputs
        if dataType == "shapefile":
            arcpy.AddIDMessage("ERROR this is not a valid type")
            return

        if dataType != "featureclass" or desc.shapeType.lower() != "point":
            arcpy.AddIDMessage("ERROR this is not a valid type")

            return

        # check if it's a service or feature class in db
        # Check the domains to see if they exist and are valid
        # will update if necessary

        if r'/rest/services' not in arcpy.Describe(feature_layer).catalogPath:
            geodatabase = get_geodatabase_path(feature_layer)
            check_and_create_domains(geodatabase)

        # Add the fields

        # Add Wet Weather metadata fields
        existingFields = [
            field.name for field in arcpy.ListFields(feature_layer)]

        if 'Inspected_By1' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'Inspected_By1',
                                      field_type="TEXT",
                                      field_alias='Inspector-1:',
                                      field_is_nullable="NULLABLE",
                                      field_domain="Inspector"
                                      )
        if 'Inspected_By2' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'Inspected_By2',
                                      field_type="TEXT",
                                      field_alias='Inspector-2:',
                                      field_is_nullable="NULLABLE",
                                      field_domain="Inspector"
                                      )
        if 'Inspec_Num' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'Inspec_Num',
                                      field_type="DOUBLE",
                                      field_alias='Wet Weather Inspection #:',
                                      field_is_nullable="NULLABLE",
                                      )
        if 'Clear_Flow' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'Clear_Flow',
                                      field_type="TEXT",
                                      field_alias='Clear Flow In Manhole:',
                                      field_is_nullable="NULLABLE",
                                      field_domain="Yes_No"
                                      )

        if 'ESRISNSR_AZIMUTH' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRISNSR_AZIMUTH',
                                      field_type="DOUBLE",
                                      field_alias='Compass reading (°)',
                                      field_is_nullable="NULLABLE"
                                      )

        # Update fields with Domains

        # Update GNSS metadata fields with Domains
        domainFields = [field for field in arcpy.ListFields(feature_layer) if field.name == 'ESRIGNSS_FIXTYPE' or
                        field.name == 'ESRIGNSS_STATIONID' or field.name == 'ESRIGNSS_NUMSATS' or field.name == 'ESRIGNSS_POSITIONSOURCETYPE']

        for field in domainFields:
            if field.name == 'ESRIGNSS_FIXTYPE' and not field.domain:
                arcpy.AssignDomainToField_management(
                    feature_layer, field, 'ESRI_FIX_TYPE_DOMAIN')
                continue

            if field.name == 'ESRIGNSS_STATIONID' and not field.domain:
                arcpy.AssignDomainToField_management(
                    feature_layer, field, 'ESRI_STATION_ID_DOMAIN')
                continue

            if field.name == 'ESRIGNSS_NUMSATS' and not field.domain:
                arcpy.AssignDomainToField_management(
                    feature_layer, field, 'ESRI_NUM_SATS_DOMAIN')
                continue

            if field.name == 'ESRIGNSS_POSITIONSOURCETYPE' and not field.domain:
                arcpy.AssignDomainToField_management(
                    feature_layer, field, 'ESRI_POSITIONSOURCETYPE_DOMAIN')
                continue

    except Exception as e:
        arcpy.AddError("{}\n".format(e))
        return


if __name__ == "__main__":
    """
        Commandline use to add fields to a layer

        Input: layer names (fully qualified paths)

        Example: python add_gps_fields "C:/temp/test.gdb/test" "C:/temp/test.gdb/test2"
    """
    parser = argparse.ArgumentParser(
        "Add Wet Weather Fields to Feature Layers")
    parser.add_argument("layers", nargs='+',
                        help="The layers to add fields to")
    args = parser.parse_args()
    for layer in args.layers:
        wet_weather(layer)
