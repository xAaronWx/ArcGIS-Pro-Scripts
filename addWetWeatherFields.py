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
            if domain.name == 'Yes_N0':
                # check if cvs 0,1,2,4,5 are in the codedValues
                values = [cv for cv in domain.codedValues]
                if not set(set([0, 1, 2, 4, 5])).issubset(values):
                    arcpy.AddIDMessage("ERROR",355)
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

    # Check if 'NumSats" is a domain, if so check the range
    if 'ESRI_NUM_SATS_DOMAIN' in domain_names:
        if domain.name == "ESRI_NUM_SATS_DOMAIN":
            if domain.range[0] != 0 or domain.range[1] != 99:
                arcpy.AddIDMessage("ERROR",355)
                return
    else:
        # Add the domain and set the range
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="ESRI_NUM_SATS_DOMAIN",
                                      domain_description="Number of Satellites",
                                      field_type="SHORT",
                                      domain_type="RANGE",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")
        arcpy.SetValueForRangeDomain_management(geodatabase, "ESRI_NUM_SATS_DOMAIN", 0, 99)
    # Check if 'StationID" is a domain, if so check the range
    if 'ESRI_STATION_ID_DOMAIN' in domain_names:
        if domain.name == "ESRI_STATION_ID_DOMAIN":
            if domain.range[0] != 0 or domain.range[1] != 1023:
                arcpy.AddIDMessage("ERROR",355)
                return
    else:
        # Add the domain and set the range
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="ESRI_STATION_ID_DOMAIN",
                                      domain_description="Station ID",
                                      field_type="SHORT",
                                      domain_type="RANGE",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")
        arcpy.SetValueForRangeDomain_management(geodatabase, "ESRI_STATION_ID_DOMAIN", 0, 1023)
    if 'ESRI_POSITIONSOURCETYPE_DOMAIN' in domain_names:
        for domain in domains:
            if domain.name == 'ESRI_POSITIONSOURCETYPE_DOMAIN':
                # check if cvs 0,1,2,3,4 are in the codedValues
                values = [cv for cv in domain.codedValues]
                if not set(set([0, 1, 2, 3, 4])).issubset(values):
                    arcpy.AddError("ESRI_POSITIONSOURCETYPE_DOMAIN is missing a coded value pair.")
                    return
    else:
        # Add the domain and values
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="ESRI_POSITIONSOURCETYPE_DOMAIN",
                                      domain_description="Position Source Type",
                                      field_type="SHORT",
                                      domain_type="CODED",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")

        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_POSITIONSOURCETYPE_DOMAIN",
                                               code="0",
                                               code_description="Unknown")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_POSITIONSOURCETYPE_DOMAIN",
                                               code="1",
                                               code_description="User defined")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_POSITIONSOURCETYPE_DOMAIN",
                                               code="2",
                                               code_description="Integrated (System) Location Provider")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_POSITIONSOURCETYPE_DOMAIN",
                                               code="3",
                                               code_description="External GNSS Receiver")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_POSITIONSOURCETYPE_DOMAIN",
                                               code="4",
                                               code_description="Network Location Provider")

def add_gnss_fields(feature_layer):
    """
    This adds specific fields required for GPS units to
        auto-populate in collector application

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
            dataType = arcpy.Describe(feature_layer).dataElement.dataType.lower()

        # catch invalid inputs
        if dataType == "shapefile":
            arcpy.AddIDMessage("ERROR", 656)
            return

        if dataType != "featureclass" or desc.shapeType.lower() != "point":
            arcpy.AddIDMessage("ERROR", 347)

            return

        # check if it's a service or feature class in db
        # Check the domains to see if they exist and are valid
        # will update if necessary

        if r'/rest/services' not in arcpy.Describe(feature_layer).catalogPath:
            geodatabase = get_geodatabase_path(feature_layer)
            check_and_create_domains(geodatabase)

        # Add the fields

        # Add GNSS metadata fields
        existingFields = [field.name for field in arcpy.ListFields(feature_layer)]


        if 'Clear_Flow' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'Clear_Flow',
                                      field_type="TEXT",
                                      field_alias='Clear Flow In Manhole:',
                                      field_is_nullable="NULLABLE",
                                      field_domain="Yes_No"
                                      )

        if 'ESRIGNSS_RECEIVER' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_RECEIVER',
                                      field_type="STRING",
                                      field_length=50,
                                      field_alias='Receiver Name',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_LATITUDE' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_LATITUDE',
                                      field_type="DOUBLE",
                                      field_alias='Latitude',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_LONGITUDE' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_LONGITUDE',
                                      field_type="DOUBLE",
                                      field_alias='Longitude',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_ALTITUDE' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_ALTITUDE',
                                      field_type="DOUBLE",
                                      field_alias='Altitude',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_H_RMS' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_H_RMS',
                                      field_type="DOUBLE",
                                      field_alias='Horizontal Accuracy (m)',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_V_RMS' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_V_RMS',
                                      field_type="DOUBLE",
                                      field_alias='Vertical Accuracy (m)',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_FIXDATETIME' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_FIXDATETIME',
                                      field_type="Date",
                                      field_alias='Fix Time',
                                      field_is_nullable="NULLABLE",
                                      )

        if 'ESRIGNSS_FIXTYPE' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_FIXTYPE',
                                      field_type="SHORT",
                                      field_alias='Fix Type',
                                      field_is_nullable="NULLABLE",
                                      field_domain = "ESRI_FIX_TYPE_DOMAIN"
                                      )

        if 'ESRIGNSS_CORRECTIONAGE' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_CORRECTIONAGE',
                                      field_type="DOUBLE",
                                      field_alias='Correction Age',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_STATIONID' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_STATIONID',
                                      field_type="SHORT",
                                      field_alias='Station ID',
                                      field_is_nullable="NULLABLE",
                                      field_domain = "ESRI_STATION_ID_DOMAIN"
                                      )

        if 'ESRIGNSS_NUMSATS' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_NUMSATS',
                                      field_type="SHORT",
                                      field_alias='Number of Satellites',
                                      field_is_nullable="NULLABLE",
                                      field_domain="ESRI_NUM_SATS_DOMAIN"
                                      )

        if 'ESRIGNSS_PDOP' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_PDOP',
                                      field_type="DOUBLE",
                                      field_alias='PDOP',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_HDOP' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_HDOP',
                                      field_type="DOUBLE",
                                      field_alias='HDOP',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_VDOP' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_VDOP',
                                  field_type="DOUBLE",
                                  field_alias='VDOP',
                                  field_is_nullable="NULLABLE"
                                  )

        if 'ESRIGNSS_DIRECTION' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_DIRECTION',
                                      field_type="DOUBLE",
                                      field_alias='Direction of travel (°)',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_SPEED' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_SPEED',
                                      field_type="DOUBLE",
                                      field_alias='Speed (km/h)',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRISNSR_AZIMUTH' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRISNSR_AZIMUTH',
                                      field_type="DOUBLE",
                                      field_alias='Compass reading (°)',
                                      field_is_nullable="NULLABLE"
                                      )

        if 'ESRIGNSS_AVG_H_RMS' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_AVG_H_RMS',
                                      field_type="DOUBLE",
                                      field_alias='Average Horizontal Accuracy (m)',
                                      field_is_nullable="NULLABLE",
                                      )

        if 'ESRIGNSS_AVG_V_RMS' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_AVG_V_RMS',
                                      field_type="DOUBLE",
                                      field_alias='Average Vertical Accuracy (m)',
                                      field_is_nullable="NULLABLE",
                                      )

        if 'ESRIGNSS_AVG_POSITIONS' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_AVG_POSITIONS',
                                      field_type="SHORT",
                                      field_alias='Averaged Positions',
                                      field_is_nullable="NULLABLE",
                                      )

        if 'ESRIGNSS_H_STDDEV' not in existingFields:
            arcpy.AddField_management(feature_layer,
                                      'ESRIGNSS_H_STDDEV',
                                      field_type="DOUBLE",
                                      field_alias='Standard Deviation (m)',
                                      field_is_nullable="NULLABLE",
                                      )

        # Update fields with Domains

        # Update GNSS metadata fields with Domains
        domainFields = [field for field in arcpy.ListFields(feature_layer) if field.name == 'ESRIGNSS_FIXTYPE' or \
                          field.name == 'ESRIGNSS_STATIONID' or field.name == 'ESRIGNSS_NUMSATS' or field.name == 'ESRIGNSS_POSITIONSOURCETYPE']

        for field in domainFields:
            if field.name == 'ESRIGNSS_FIXTYPE' and not field.domain:
                arcpy.AssignDomainToField_management(feature_layer, field, 'ESRI_FIX_TYPE_DOMAIN')
                continue

            if field.name == 'ESRIGNSS_STATIONID' and not field.domain:
                arcpy.AssignDomainToField_management(feature_layer, field, 'ESRI_STATION_ID_DOMAIN')
                continue

            if field.name == 'ESRIGNSS_NUMSATS' and not field.domain:
                arcpy.AssignDomainToField_management(feature_layer, field, 'ESRI_NUM_SATS_DOMAIN')
                continue

            if field.name == 'ESRIGNSS_POSITIONSOURCETYPE' and not field.domain:
                arcpy.AssignDomainToField_management(feature_layer, field, 'ESRI_POSITIONSOURCETYPE_DOMAIN')
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
    parser = argparse.ArgumentParser("Add GPS Fields to Feature Layers")
    parser.add_argument("layers", nargs='+', help="The layers to add fields to")
    args = parser.parse_args()
    for layer in args.layers:
        add_gnss_fields(layer)
