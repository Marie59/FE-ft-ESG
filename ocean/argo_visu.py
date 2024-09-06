##########################
### Data visualisation ###
##########################

## Trajectories ##
from argopy import DataFetcher, IndexFetcher

idx = IndexFetcher().float([6902745, 6902746]).load()
fig, ax = idx.plot('trajectory')
fig, ax = idx.plot()  # Trajectory is the default plot

## Histograms on properties ##
# It is also possible to create horizontal bar plots for histograms on some data properties: profiler and dac:
idx = IndexFetcher().region([-80,-30,20,50,'2021-01','2021-08']).load()
fig, ax = idx.plot('dac')

# If you have Seaborn installed, you can change the plot style:
fig, ax = idx.plot('profiler', style='whitegrid')

## Dashboards ##
# We provide access to the Euro-Argo ERIC, Ocean-OPS, Argovis and BGC dashboards with the option type. See dashboard() for all the options.

argopy.dashboard()
# or argopy.dashboard(5904797), argopy.dashboard(6902746, 12), argopy.dashboard(5903248, 3, type='bgc')

## Scatter Maps ##
# maps with Argo profile positions coloured according to specific variables

from argopy.plot import scatter_map
from argopy import DataFetcher, OceanOPSDeployments

ArgoSet = DataFetcher(mode='expert').float([6902771, 4903348]).load()
ds = ArgoSet.data.argo.point2profile()
df = ArgoSet.index

df_deployment = OceanOPSDeployments([-90, 0, 0, 90]).to_dataframe()

scatter_map(df)
scatter_map(df,
            x='longitude',
            y='latitude',
            hue='wmo',
            cmap='Set1',
            traj_axis='wmo')
            
fig, ax = scatter_map(df,
                   figsize=(10,6),
                   set_global=True,
                   markersize=2,
                   markeredgecolor=None,
                   legend_title='Floats WMO',
                   cmap='Set2')
               
# The colormap is automatically guessed using the hue argument. Here are some examples.
scatter_map(ds, hue='DATA_MODE')

scatter_map(ds,
            x='LONGITUDE',
            y='LATITUDE',
            hue='DATA_MODE',
            cmap='data_mode',
            traj_axis='PLATFORM_NUMBER')
 
ds['year'] = ds['TIME.year']  # Add new variable to the dataset
scatter_map(ds,
            hue='year',
            cmap='Spectral_r',
            legend_title='Year of sampling')
            
## Argo colors ##            
ArgoColors('data_mode')           
ArgoColors('qc_flag')
ArgoColors('deployment_status')
ArgoColors('months')
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
