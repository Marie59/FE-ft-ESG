##############################
### Working with Argo data ###
##############################
# Once you fetched data, argopy comes with a handy xarray.Dataset accessor argo to perform specific manipulation of the data. 

## Manipulating data ##
# Transforming from 1D (default) to 2D

argo_points = argo_data.data
argo_profiles = argo_points.argo.point2profile()

# Pressure levels: Interpolation
# Once your dataset is a collection of vertical profiles, you can interpolate variables on standard pressure levels 

argo_interp = argo_profiles.argo.interp_std_levels([0,10,20,30,40,50])

argo_interp

# Pressure levels: Group-by bins


# Filters



# Complementary data


# Data models


# Saving data

