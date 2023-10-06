import pyvo as vo



CAOMTAP = 'http://vao.stsci.edu/CAOMTAP/TapService.aspx'

def fetch_obspointing(mission: str,
                      constraints: str):
    """TAP query to get table results for a particular mission"""

    tap = vo.dal.TAPService(CAOMTAP)
    query = f"""SELECT obs_id, obs_collection, instrument_name, filters, s_ra, s_dec, t_min, t_max, s_region
FROM dbo.ObsPointing 
WHERE obs_collection='{mission}' 
{constraints}"""
    print(query)
    results = tap.search(query)
    temp = results.to_table()
    return temp.to_pandas()
