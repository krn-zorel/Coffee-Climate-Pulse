import os
import pandas as pd
import joblib

# These are just creating reusable strings for our file paths
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT)
PROC = os.path.join(BASE, 'data', 'processed')
MDL = os.path.join(BASE, 'models')

df_env_country  = pd.read_csv(os.path.join(PROC, 'env_yearly_country.csv'))
df_env_location = pd.read_csv(os.path.join(PROC, 'env_yearly_location.csv'))
df_fao          = pd.read_csv(os.path.join(PROC, 'fao_yield_clean.csv'))
df_chem         = pd.read_csv(os.path.join(PROC, 'chem_processed.csv'))
df_health       = pd.read_csv(os.path.join(PROC, 'bio_full.csv'))

price_model    = joblib.load(os.path.join(MDL, 'price_predictor.pkl'))
price_features = joblib.load(os.path.join(MDL, 'price_features.pkl'))
le_env         = joblib.load(os.path.join(MDL, 'country_encoder_env.pkl'))

hr_model       = joblib.load(os.path.join(MDL, 'heart_rate_predictor.pkl'))
health_scaler  = joblib.load(os.path.join(MDL, 'health_scaler.pkl'))
health_feats   = joblib.load(os.path.join(MDL, 'health_features.pkl'))

quality_model   = joblib.load(os.path.join(MDL, 'quality_scorer.pkl'))
quality_feats   = joblib.load(os.path.join(MDL, 'quality_features.pkl'))
radar_cols      = joblib.load(os.path.join(MDL, 'radar_cols.pkl'))



YEARS = [int(y) for y in sorted(df_fao['Year'].dropna().unique())]
ENV_COUNTRIES = sorted(df_env_country['Country'].dropna().unique())
CHEM_COUNTRIES = sorted(df_chem['Country'].dropna().unique())

SQ_MAP = {'Poor': 1, 'Fair': 2, 'Good': 3, 'Excellent': 4}
SL_MAP = {'Low':  1, 'Medium': 2, 'High': 3}

C = {
    'bg':     '#0A0A0A',
    'card':   '#141414',
    'border': '#2A2A2A',
    'text':   '#F0EAD6',
    'muted':  '#888888',
    'accent': '#F5A623',
    'earth':  '#8B6914',
    'red':    '#E84855',
    'blue':   '#2E86AB',
    'green':  '#27AE60',
}