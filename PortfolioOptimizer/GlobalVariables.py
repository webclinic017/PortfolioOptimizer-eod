"""
Global variables to use throughout.
"""

# User options
INVESTMENT_CHOICES = ['Global Stocks', 'US Stocks', 'DM Stocks', 'EM Stocks', # stocks
                      'US Large Cap Stocks', 'US Small Cap Stocks',
                      'US Value Stocks', 'US Growth Stocks',
                      'Global Bonds', 'US Bonds', 'ex-US Bonds', # bonds
                      'US Treasuries', 'US Investment Grade Bonds', 'US High Yield Bonds',
                      'TIPS',
                      'Commodities', 'Oil', 'Gold', # commodities
                      'Bitcoin', 'Ethereum'] # crypto
OBJECTIVE_CHOICES = ['Max Sharpe Ratio (Return/Risk)', '90% Stock / 10% Bond Equivalent',
                         '80% Stock / 20% Bond Equivalent', '70% Stock / 30% Bond Equivalent',
                         '60% Stock / 40% Bond Equivalent', '50% Stock / 50% Bond Equivalent',
                         '40% Stock / 60% Bond Equivalent', '30% Stock / 70% Bond Equivalent',
                         '20% Stock / 80% Bond Equivalent', '10% Stock / 90% Bond Equivalent']
OPTIMIZER_CHOICES = ['Bootstrapping']

# User defaults
DEFAULT_INVESTMENTS = ['US Stocks', 'DM Stocks', 'EM Stocks', 'Global Bonds',
                                'Commodities', 'Real Estate']
DEFAULT_OBJECTIVE = 'Max Sharpe Ratio (Return/Risk)'
DEFAULT_OPTIMIZER_OPTIONS = ['Bootstrapping']

# Security mapping
SECURITY_MAPPING = {'Global Stocks': 'ACWI.US', # iShares MSCI ACWI
                    'US Stocks': 'IWV.US', # iShares Russell 3000
                    'DM Stocks': 'ACWX.US', # iShares MSCI ACWI ex U.S.
                    'EM Stocks': 'EEM.US', # iShares MSCI Emerging Markets
                    'US Large Cap Stocks': 'IWB.US', # iShares Russell 1000
                    #'US Mid Cap Stocks': 'IWR.US', # iShares Russell Midcap (subset of IWB)
                    'US Small Cap Stocks': 'IWM.US', # iShares Russell 2000
                    'US Value Stocks': 'RPV.US', # Invesco S&P 500 Pure Value
                    'US Growth Stocks': 'RPG.US', # Invesco S&P 500 Pure Growth
                    'Global Bonds': 'BNDW.US', # Vanguard Total World Bond (Bloomberg Global
                                               # Aggregate Float Adjusted Composite Index)
                    'US Bonds': 'BND.US', # Vanguard Total Bond Market (Bloomberg U.S. Aggregate
                                          # Bond Index)
                    'ex-US Bonds': 'BNDX.US', # Vanguard Total International Bond (Bloomberg Global
                                           # Aggregate ex-USD Float Adjusted RIC Capped Index (USD
                                           # Hedged)
                    'US Treasuries': 'GOVT.US', # iShares Core U.S. Treasury Bond (ICE US Treasury
                                                # Core Bond Index)
                    'US Investment Grade Bonds': 'LQD.US', # iShares iBoxx $ Investment Grade
                                                           # Corporate (Markit iBoxx USD Liquid
                                                           # Investment Grade Index)
                    'US High Yield Bonds': 'HYG.US', # iShares iBoxx $ High Yield Corporate Bond
                                                     # (Markit iBoxx USD Liquid High Yield Index)
                    'TIPS': 'TIP.US', # iShares TIPS Bond (Bloomberg U.S. Treasury Inflation
                                      # Protected Securities (TIPS) Index
                    'Commodities': 'GSG.US', # iShares S&P GSCI Commodity-Indexed Trust
                    'Oil': 'USO.US', # United States Oil Fund
                    'Gold': 'GLD.US', # SPDR Gold Shares
                    #'Real Estate': Not currently done since all ETFs are only invested in REITs,
                    #               not actual real estate and so this is covered in stocks.
                    'Bitcoin': 'BITO.US', # ProShares Bitcoin
                    'Ethereum': 'ETHE.US'} # Grayscale Ethereum Trust


