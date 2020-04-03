import requests
import pandas as pd


inp_file = 'input_files/Paphos.csv'
out_file = 'output_files/Paphos_out.csv'
null_value = -1
df = pd.read_csv(inp_file)
post_codes = df['Postcode'].fillna(null_value).astype(int)
areas = df['Area']
query_terms_dct = {}
query_terms = []
len_post_codes = len(post_codes)
len_areas = len(areas)
url_prefix = 'https://maps.googleapis.com/maps/api/geocode/json?address='
url_suffix = '&key=AIzaSyBuB6NTwnsieCYE0GDLf_4BwWowtFAaFLM'


if (len_post_codes != len_areas):
	raise Exception("Different lengths of post_codes and areas. Please fix this.")

# Geerate the query_terms_dct in the format: post_code ->  'area'
for i in range(0, len_post_codes):
	curr_post_code = post_codes[i]

	# Get only the unique post codes
	if curr_post_code != null_value:
		if curr_post_code not in query_terms_dct:
			query_terms_dct[curr_post_code] = str(areas[i])

# Generate the query_terms in the format 'post_code+area'
query_terms = [(str(k) + '+' + query_terms_dct[k]) for k in query_terms_dct]

list_post_codes = []
list_lat = []
list_lng = []

# Generate the url needed for each call to the Geocoding API
for qt in query_terms:
	url = url_prefix + qt + url_suffix
	print("Will request url: ", url)

	req = requests.get(url)
	res = req.json()

	try:
		result = res['results'][0]


		post_code = qt.split('+')[0]
		list_post_codes.append(post_code)
		list_lat.append(result['geometry']['location']['lat'])
		list_lng.append(result['geometry']['location']['lng'])
	except Exception as e:
		print("Couldn't process this entry. Reason: ", str(e))
		continue


out_data = {
	'post_code': list_post_codes,
    'lat': list_lat,
    'lng': list_lng
}

# Export to csv
df = pd.DataFrame(out_data, columns= ['post_code', 'lat', 'lng'])
df.to_csv (out_file, index = False, header=True)
print("File created: ", out_file)
