import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import colorlover as cl
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os.path
import sys
import plotly.graph_objects as go
import plotly.express as px
import colorlover as cl
from IPython.display import HTML
import plotly.offline as ply
import plotly.graph_objs as go
from plotly.tools import make_subplots
sys.path.insert(0, os.path.abspath('../../'))
from util.db.mysql_api import SQL
from datetime import datetime
from common.retailer_analytics import get_active_retailers
from common.campaign import get_current_campaigns, campaign_parameters
from common.user_journeys import get_journeys, select_journeys, map_journey, map_journey_points
from common.user_activity import get_users, users_activity, analyse_incomplete_scans
from common.trial_management import get_signups, get_participants, get_trials, define_trial, existing_groups, build_group, populate_groups, match_users
from common.value_attribution import get_journey_properties, aggregate_properties
from common.rfid_processing import get_bag_use, get_fp_bags, stock_check, get_aggregated_scans, get_deduped_bags, aggregate_rescans, count_bags_weekdays, count_bags_hours, count_bags_daily, select_site_type, week_by_week
from common.bag_distribution_plots import plot_retailer_map, plot_campaign_summary, plot_campaign_bags, plot_all_campaign_bags, plot_all_campaign_bags_corrected, plot_stock, plot_distributed, plot_weekdays, plot_hourly


def monitor_campaign(cdb1): 
    
    
    st.title('Monitor Campaign Progress')
   
    #Task 1 (1a) Select campaign and extract relevant campaign data including number of bags bought. 
    dt = datetime.now()
    current_campaign = get_current_campaigns(dt,cdb1)
    
    active_sites = get_active_retailers(cdb1)
    
    campaign_name = st.sidebar.selectbox('Choose campaign',active_sites['campaign_name'].unique(),index = 2) 
    campaign_id = active_sites.loc[active_sites['campaign_name'] == campaign_name, 'campaign_id'].iloc[0]
    campaigns = [campaign_id]
    
    parameters = campaign_parameters(campaigns,cdb1)
    
    active_sites = active_sites[active_sites['campaign_id'].isin(campaigns)]
    asi = active_sites['site_name'].unique().tolist()
    
    sites = st.sidebar.multiselect('Choose retailers',options = asi,default = asi)
    sites = list(map(str, sites)) 
    
    selected_active_sites = active_sites[active_sites['site_name'].isin(sites)]
    
    if st.sidebar.button('Filter by date'):
        analysis_start_day = st.sidebar.date_input('Analysis start date')
    else:
        analysis_start_day = parameters.loc[parameters['campaign_id'] == campaign_id, 'campaign_start'].iloc[0].date()
       
    
    #Task 2
    bags = bag_usage(analysis_start_day,campaigns,cdb1)
     
    
    plot_all_campaign_bags(bags,campaigns,selected_active_sites)
    if st.sidebar.button('Filter by date'):
        analysis_start_day = st.sidebar.date_input('Analysis start date')
    else:
        analysis_start_day = parameters.loc[parameters['campaign_id'] == campaign_id,'campaign_start'].iloc[0].date()

        bags = bag_usage(analysis_start_day,campaigns,cdb1)
        plot_all_campaign_bags(bags,campaigns,sites)

   #Task 3 
    select_journeys(analysis_start_day,campaigns,cdb1)

    ...
    journeys = select_journeys(analysis_start_day,campaigns,cdb1)
	...
    #Task 4
    get_journey_properties(cdb1,uids)
	…
	uids = journeys['user_id'].unique().tolist()
	properties = get_journey_properties(cdb1,uids)
	…




#Commercial
#Number of bags distributed and comparison with number of bags bought
#Impressions generated vs target impressions by type (See, Engage, Impact)4
chosen_colors=cl.scales['5']['qual'][np.random.choice(list(cl.scales['5']['qual'].keys()))]


data=[]

trace_names=['generated', 'impressions']

for i in range(2):
    data.append(
        go.Histogram(
            x=campaign_id[(campaign_id.campaign_type==trace_names[i]) & (campaign_id.duration_min<60)].duration_min,
            name=trace_names[i],
            marker=dict(
                color=chosen_colors[i]
            ),
            opacity=0.5
        )
    )

layout = go.Layout(
    title='Distribution of bags ',
    barmode='overlay',
    xaxis=dict(
        title='count_bags_hours'
    ),
    yaxis=dict(
        title='Count'
    ),
    
    )
  st.plotly_chart(figure)