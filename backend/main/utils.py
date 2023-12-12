import os
import numpy as np
from django.core.exceptions import ValidationError
from osgeo import gdal, osr

from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj


def upload_to(instance, filename):
    return 'vector/%s/%s' % (instance.user.username, filename)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.tif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    
    
def normalize_ar(ar):
    array = (ar - ar.min()) / (ar.max() - ar.min())
    ar[ar > 1] = 1
    ar[ar < 0] = 0
    array = array * 255
    array = array.astype(np.uint8)
    return array


def get_bounds(file):
    ds = gdal.Open(file)
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel
    poly = Polygon([[xmin, ymax], [xmax, ymax], [xmax, ymin], [xmin, ymin]])
    proj = osr.SpatialReference(wkt=ds.GetProjection())
    epsg = proj.GetAttrValue('AUTHORITY', 1)
    if int(epsg) != 4326:

        wgs84 = pyproj.CRS('EPSG:4326')
        utm = ds.GetProjection()

        project = pyproj.Transformer.from_crs(
            utm, wgs84, always_xy=True
        ).transform
        poly = transform(project, poly)

    return poly.bounds