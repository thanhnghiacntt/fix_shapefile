# -*- coding: utf-8 -*-
import geopandas as gpd
from shapely.validation import explain_validity
from shapely.geometry import Polygon

# Đọc shapefile từ đường dẫn đầy đủ
file_path = "G:/Temp/water-polygons-split-3857/water_polygons.shp"
gdf = gpd.read_file(file_path)

# Kiểm tra hình học không hợp lệ
gdf['is_valid'] = gdf.is_valid
invalid_geoms = gdf[~gdf['is_valid']]

# Hiển thị các hình học không hợp lệ và lý do
for idx, row in invalid_geoms.iterrows():
    reason = explain_validity(row.geometry)
    print(f"Index {idx}: {reason}")

# Sửa lỗi hình học
def fix_geometry(geom):
    if not geom.is_valid:
        return geom.buffer(0)
    return geom

gdf['geometry'] = gdf['geometry'].apply(fix_geometry)

# Kiểm tra lại hình học sau khi sửa
gdf['is_valid'] = gdf.is_valid
still_invalid = gdf[~gdf['is_valid']]
if still_invalid.empty:
    print("Tất cả hình học đều hợp lệ sau khi sửa.")
else:
    print("Vẫn còn hình học không hợp lệ sau khi sửa.")
    for idx, row in still_invalid.iterrows():
        reason = explain_validity(row.geometry)
        print(f"Index {idx}: {reason}")

# Lưu lại shapefile đã sửa
output_file_path = "G:/Temp/water-polygons-split-3857/after/water_polygons.shp"
gdf.to_file(output_file_path)
