"""
Global variables to use throughout.
"""

# User options
# Security mapping is {Investment Type: (ETF Ticker, ETF Name)}
SECURITY_MAPPING = {'Global Stocks': ('ACWI.US', 'iShares MSCI ACWI', '0.33%'),
                    'US Stocks': ('IWV.US', 'iShares Russell 3000', '0.20%'),
                    'DM Stocks': ('ACWX.US', 'iShares MSCI ACWI ex U.S.', '0.33%'),
                    'EM Stocks': ('EEM.US', 'iShares MSCI Emerging Markets', '0.68%'),
                    'US Large Cap Stocks': ('IWB.US', 'iShares Russell 1000', '0.15%'),
                    #'US Mid Cap Stocks': ('IWR.US', 'iShares Russell Midcap (subset of IWB)'),
                    'US Small Cap Stocks': ('IWM.US', 'iShares Russell 2000', '0.19%'),
                    'US Value Stocks': ('RPV.US', 'Invesco S&P 500 Pure Value', '0.35%'),
                    'US Growth Stocks': ('RPG.US', 'Invesco S&P 500 Pure Growth', '0.35%'),
                    'Global Bonds': ('BNDW.US', 'Vanguard Total World Bond (Bloomberg Global '
                                                'Aggregate Float Adjusted Composite Index)',
                                     '0.06%'),
                    'US Bonds': ('BND.US', 'Vanguard Total Bond Market (Bloomberg U.S. Aggregate '
                                           'Bond Index)', '0.03%'),
                    'ex-US Bonds': ('BNDX.US', 'Vanguard Total International Bond (Bloomberg Global '
                                               'Aggregate ex-USD Float Adjusted RIC Capped Index ('
                                               'USD Hedged)', '0.07%'),
                    'US Treasuries': ('GOVT.US', 'iShares Core U.S. Treasury Bond (ICE US Treasury '
                                                 'Core Bond Index)', '0.05%'),
                    'US Investment Grade Bonds': ('LQD.US', 'iShares iBoxx $ Investment Grade '
                                                            'Corporate (Markit iBoxx USD Liquid '
                                                            'Investment Grade Index)', '0.14%'),
                    'US High Yield Bonds': ('HYG.US', 'iShares iBoxx $ High Yield Corporate Bond '
                                                      '(Markit iBoxx USD Liquid High Yield '
                                                      'Index)', '0.48%'),
                    'TIPS': ('TIP.US', 'iShares TIPS Bond (Bloomberg U.S. Treasury Inflation '
                                       'Protected Securities (TIPS) Index)', '0.19%'),
                    'Commodities': ('GSG.US', 'iShares S&P GSCI Commodity-Indexed Trust', '0.75%'),
                    'Oil': ('USO.US', 'United States Oil Fund', '0.45%'),
                    'Gold': ('GLD.US', 'SPDR Gold Shares', '0.40%'),
                    #'Real Estate': Not currently done since all ETFs are only invested in REITs,
                    #               not actual real estate and so this is covered in stocks.
                    'Bitcoin': ('BITO.US', 'ProShares Bitcoin', '0.95%'),
                    'Ethereum': ('ETHE.US', 'Grayscale Ethereum Trust', '2.50%')}
OBJECTIVE_CHOICES = {'Max Sharpe Ratio (Return/Risk)': np.dot(x, returns) /
                                                       np.sqrt(),
                     '90% Stock / 10% Bond Equivalent',
                     '80% Stock / 20% Bond Equivalent',
                     '70% Stock / 30% Bond Equivalent',
                     '60% Stock / 40% Bond Equivalent',
                     '50% Stock / 50% Bond Equivalent',
                     '40% Stock / 60% Bond Equivalent',
                     '30% Stock / 70% Bond Equivalent',
                     '20% Stock / 80% Bond Equivalent',
                     '10% Stock / 90% Bond Equivalent'}
OPTIMIZER_CHOICES = ['Bootstrapping']

# User defaults
DEFAULT_INVESTMENTS = ['US Stocks', 'DM Stocks', 'EM Stocks', 'Global Bonds',
                       'Commodities']
DEFAULT_OBJECTIVE = 'Max Sharpe Ratio (Return/Risk)'
DEFAULT_OPTIMIZER_OPTIONS = ['Bootstrapping']

# Imputation defaults
DEFAULT_IMPUTE_COUNT = 5




