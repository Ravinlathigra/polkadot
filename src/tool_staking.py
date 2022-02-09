import plotly.express as px 
import numpy as np
import pandas as pd

class inflation():
    def __init__(self,baseline_inflation,ideal_inflation,ideal_staking,distance_metric):
        self.baseline_inflation = baseline_inflation
        self.ideal_inflation = ideal_inflation
        self.ideal_staking = ideal_staking
        self.distance_metric = distance_metric


    def extract_values(self,actual_staking):
        i_right= self.baseline_inflation + (self.ideal_inflation*self.ideal_staking- self.baseline_inflation)*(2**((self.ideal_staking-actual_staking)/self.distance_metric))
        i_left = self.baseline_inflation + (actual_staking*(self.ideal_inflation- (self.baseline_inflation/self.ideal_staking)))
        
        i_nomin = min(i_left,i_right)

        i_yield = i_nomin/actual_staking
        rate_dict = {'linear_grade':i_left,
                     'exp_grade':i_right,
                     'inflation':i_nomin,
                     'annual_yield':i_yield
                     }
        return rate_dict

    def create_df(self,lb,ub,steps):
        rate_dict = {}
        for actual_staking in np.linspace(lb,ub,steps):
            rate_dict[actual_staking] = self.extract_values(actual_staking)
        
        df = pd.DataFrame.from_dict(rate_dict,orient = "index").reset_index().rename(columns = {"index":"staked_proportion"})
        return df

    def plot_staking_rewards(self,title = "Staking Rewards"):
        color_discrete_map={'linear_grade': '#b7bfac', 
                            'exp_grade': '#aeb3b5', 
                            'inflation': '#430ceb',
                            'annual_yield': '#E6007A',
                            }

        line_dash_map={'linear_grade': 'dot', 
                            'exp_grade': 'dot', 
                            'inflation': 'solid',
                            'annual_yield': 'solid',
                            }

        coords = self.create_df(.1,1,100)
        coords = coords.melt(id_vars = 'staked_proportion')
        fig = px.line(coords,x = "staked_proportion",y = "value", line_dash = 'variable',color = "variable", title=title,color_discrete_map=color_discrete_map,line_dash_map=line_dash_map)
        fig.update_yaxes(range=[0, 1])
        fig.layout.template = 'plotly_dark'
        fig.update_xaxes(title = "Proportion of DOT Staked") #title_font_family
        fig.update_yaxes(title = "Annual Rate") #title_font_family

        return fig


if __name__ == "__main__":
    # df = calculate_yield()
    inf = inflation(.025,.2,.5,.05)
    yield_curves = inf.plot_staking_rewards(title = "Polkadot Staking Rewards")
    yield_curves.show()

