"""
Global variables to use throughout.
"""

# User options
INVESTMENT_CHOICES = ['Global Stocks', 'US Stocks', 'DM Stocks', 'EM Stocks', # stocks
                      'US Large Cap Stocks', 'US Mid Cap Stocks', 'US Small Cap Stocks',
                      'US Value Stocks', 'US Growth Stocks',
                      'Global Bonds', 'US Bonds', 'DM Bonds', 'EM Bonds', # bonds
                      'US Treasuries', 'US Investment Grade Bonds', 'US High Yield Bonds',
                      'TIPS',
                      'Commodities', 'Oil', 'Gold', # commodities
                      'Real Estate', # real estate
                      'Bitcoin', 'Ethereum'] # crypto
TARGET_METRIC_CHOICES = ['Max Sharpe Ratio (Return/Risk)', '90% Stock / 10% Bond Equivalent',
                         '80% Stock / 20% Bond Equivalent', '70% Stock / 30% Bond Equivalent',
                         '60% Stock / 40% Bond Equivalent', '50% Stock / 50% Bond Equivalent',
                         '40% Stock / 60% Bond Equivalent', '30% Stock / 70% Bond Equivalent',
                         '20% Stock / 80% Bond Equivalent', '10% Stock / 90% Bond Equivalent']
OPTIMIZER_CHOICES = ['Bootstrapping', 'PCA']

# User defaults
DEFAULT_INVESTMENTS = ['US Stocks', 'DM Stocks', 'EM Stocks', 'Global Bonds',
                                'Commodities', 'Real Estate']
DEFAULT_TARGET_METRIC = 'Max Sharpe Ratio (Return/Risk)'
DEFAULT_OPTIMIZER_OPTIONS = ['Bootstrapping', 'PCA']