is_fy_list = ['GrossProfit', 'OperatingIncomeLoss', 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest', 
              'IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest', 'ProfitLoss', 'NetIncomeLoss', 
              'WeightedAverageNumberOfSharesOutstandingBasic', 'WeightedAverageNumberDilutedSharesOutstandingAdjustment', 'EarningsPerShareBasic', 
              'IncomeLossFromContinuingOperationsPerBasicShare', 'IncomeLossFromDiscontinuedOperationsNetOfTaxPerBasicShare', 
              'IncomeLossFromContinuingOperationsPerDilutedShare', 'IncomeLossFromDiscontinuedOperationsNetOfTaxPerDilutedShare']

cf_fy_list = ['CashAndCashEquivalentsAtCarryingValueEnding', 'CashAndCashEquivalentsAtCarryingValueBeginning', 'CashAndCashEquivalentsPeriodIncreaseDecrease',
              'NetCashProvidedByUsedInOperatingActivities', 'NetCashProvidedByUsedInInvestingActivities', 'NetCashProvidedByUsedInFinancingActivities', 
              'CashProvidedByUsedInOperatingActivitiesContinuedOperations']

is_qh_flg_lst = ['IS.InterestAndDebtExpense', 'IS.InterestExpense', 'IS.InterestExpenseDebt', 'IS.InterestExpenseRelatedParty', 
                 'IS.InterestExpenseRelatedParty', 'IS.DebtRelatedCommitmentFeesAndDebtIssuanceCosts', 'IS.FinanceCosts', 'IS.InvestmentIncomeInterestAndDividend']

working_ratio_lst = ['SelectRatioFactor', 'THIS.IS.SalesRevenueNet', 'THIS.IS.CostOfRevenue', 'THIS.IS.Investment', 'THIS.IS.Goodwill', 'THIS.IS.IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest', 'THIS.IS.AverageCashBalance', 'THIS.IS.CostOfGoodsSold', 'THIS.IS.EarningsPerShareBasic', 'THIS.IS.EarningsPerShareDiluted', 'THIS.IS.EarningsPerShareBasicAndDiluted', 'THIS.IS.RawMaterialsAndConsumablesUsed', 'THIS.IS.Profitbeforetax', 'THIS.IS.EquitySettledShareBasedPayment', 'THIS.CF.CashAndCashEquivalentsAtCarryingValueBeginning', 'THIS.IS.CostOfServices', 'THIS.BS.InvestmentProperty']

non_cummulative_lst = ['EarningsPerShareBasic', 'WeightedAverageNumberOfSharesOutstandingBasic', 'WeightedAverageNumberDilutedSharesOutstandingAdjustment', 'WeightedAverageNumberOfDilutedSharesOutstanding']

default_given_key_dict = {
                          'CLEAN_VAL':'', 
                          'TX_TAXO_PARENT':'', 
                          'GROUP_TAXO':'', 
                          'GROUP_NAME':'', 
                          'TX_LABEL':'', 
                          'TX_TAXO':'', 
                          'TABLE_TYPE':'', 
                          'SELECTION_FLAG':0, 
                          'DISPLAY_FORMAT':'n.nn', 
                          'PH_TAXO':'', 
                          'PH_LABEL':'', 
                          'CLEAN_VAL':'', 
                          'VAL_LABEL':''
                         }

matrices_static_ordered_group_lst = ['AssumptionsWACC', 'AssumptionsUsed_DCF', 'PresentValueCashFlow', 'TargetPriceCalculation', 'PeerGroupOverview', 'PeerGroupAverage', 'PE_Valuation', 'PS_Valuation', 'PBV_Valuation']   
ratios_ordered_group_lst = ['KeyFinancial','Margins','ReturnRatios','LiquidityRatios', 'SolvencyRatios', 'GrowthRatios']   
