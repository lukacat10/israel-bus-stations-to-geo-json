import csv
import json

INPUT_CSV = 'israel-public-transportation/stops.txt'
OUTPUT_JSON = 'output.geojson'
PRETTY = False


class GeoJson:
    def __init__(self):
        self.type = "FeatureCollection"
        self.features = list()  # type: list[Feature]

    def add_feature(self, feature):
        """

        :param Feature feature:
        :return:
        """
        self.features.append(feature)


class Feature:
    def __init__(self, lat, lng, title, description):
        self.type = "Feature"
        self.geometry = PointGeometry(lat, lng)
        self.properties = Properties(title, description)


class PointGeometry:
    def __init__(self, lat, lng):
        self.type = "Point"
        self.coordinates = [lng, lat]


class Properties:
    def __init__(self, title, description):
        self.title = title
        self.description = description


def columns_to_mapping(columns):
    """
    Creates a dictionary whose keys are the column names:
    stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,location_type,parent_station,zone_id

    And the values are the indexes where their appropriate entry lies in each csv row.
    :param columns:
    :return:
    """
    mapping = dict()
    for i in range(len(columns)):
        mapping[columns[i]] = i
    return mapping


def csv_line_to_feature_parameters(row_mapping, row):
    """
    Given a row mapping and a csv row, returns the needed parameters for a geojson feature:
    lat, lng, title, description

    as a list.
    :param row_mapping:
    :param row:
    :return:
    """
    returned = list()
    returned.append(row[row_mapping["stop_lat"]])
    returned.append(row[row_mapping["stop_lon"]])
    returned.append(row[row_mapping["stop_name"]])
    returned.append(row[row_mapping["stop_desc"]])
    return returned


def main():
    geojson = GeoJson()
    with open(INPUT_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        first_row = True
        mapping = None
        for row in reader:
            if first_row:
                mapping = columns_to_mapping(row)
                first_row = False
            else:
                parameters = csv_line_to_feature_parameters(mapping, row)
                feature = Feature(*parameters)
                geojson.add_feature(feature)

    with open(OUTPUT_JSON, 'w', encoding='utf8') as outputfile:
        if PRETTY:
            outputfile.write(json.dumps(geojson, default=lambda o: o.__dict__,
                                        sort_keys=False, ensure_ascii=False, indent=4))
        else:
            outputfile.write(json.dumps(geojson, default=lambda o: o.__dict__,
                                        sort_keys=False, ensure_ascii=False, separators=(',', ':')))


if __name__ == "__main__":
    main()
