### data_cleaner.py 
### Authors: DR & TV 
### Processes some data outliers before writing them to Excel file

def clean_type(p_type):
	lower = p_type.lower().strip()
	casas = ['casa', 'casas', 'house', 'habitación']
	farms = ['agricultural', 'farm', 'quinta', 'quintas o campos', 'quinta propiedad agrícultural', 'agricultural farm']
	bldgs = ['edificio', 'building']
	condos = ['condominio', 'casa-en-condominio', 'apartment', 'condo/apartment', 'apartment building', 'whole apartment building']
	depts = ['departamento', 'departamentos']
	land = ['land', 'terreno']
	offices = ['offices', 'office', 'oficina', 'oficinas']
	industrial = ['local industrial o galpón', 'galpón', 'galpon']
	commercial = ['locales comerciales', 'local comercial', 'plaza', 'plazuela', 'house with commercial space', 'sale of business']
	unspecified = ['local']
	if lower in casas:
		return 'Casa'

	elif lower in farms:
		return 'Farm'

	elif lower in bldgs:
		return "Building"

	elif lower in condos:
		return 'Condo/Apartment'

	elif lower == 'tinglado':
		return 'Shed'

	elif lower in depts:
		return 'Departamento'

	elif lower == 'deposito':
		return 'Storage'

	elif lower == 'duplex':
		return 'Duplex'

	elif lower in land:
		return 'Land'

	elif lower == 'warehouse':
		return 'Warehouse'

	elif lower == 'hotel':
		return 'Hotel'

	elif lower == 'mine':
		return 'Mine'

	elif lower in industrial:
		return 'Industrial'

	elif lower == 'rural':
		return 'Rural'

	elif lower in commercial:
		return 'Commercial'

	elif lower in offices:
		return 'Office'

	elif lower == 'plaza':
		return 'Plaza'

	elif lower == 'penthouse':
		return 'Penthouse'

	elif lower == 'proyecto':
		return 'Project'

	elif lower in unspecified:
		return 'Unspecified'

	else:
		return p_type


def clean_price(price):
	try: 
		if int(price) > 1000000000 or price == '':
			price = '0'
		else:
			return price
	except ValueError:
		return ''


def clean_dept(dept):
	santacruz = ['santa cr', 'santa cruz de la sierra', 'warnes', 'camiri', 'montero', 'la guardia', 'porongo', 'portachuelo', 'san javier']
	lapaz = ['el alto']
	cochabamba = ['cochabam']
	lower = dept.lower().strip()
	# if dept == 'Santa Cr' or dept == 'Santa Cruz de la Sierra':
	if lower in santacruz:
		return 'Santa Cruz'
	# elif dept == 'Cochabam':
	elif lower in cochabamba:
		return 'Cochabamba'
	elif lower in lapaz:
		return "La Paz"
	elif lower == '':
		return 'n/a'
	else:
		return dept


# def clean_year(year):
# 	try: 
# 		if int(year) < 1000 or int(year) > 2050:
# 			return ''
# 		else:
# 			return year
# 	except ValueError:
# 		return ''


# if __name__ == "__main__":
# 	types = ['casa', 'Casas', 'house', 'habitación', 'Quintas o campos', 'edificio', 
# 	'Condo/Apartment', 'aPaRtMeNt', 'Land', 'Terreno', 'casass', 'local', 'campo']
# 	# EO:
# 	# Casa x4 --> Farm x1 --> Building x1 --> condo/apartment x2 --> Land x2 --> Other x3
# 	prices = ['1000', '100000', '10000000', '1000000001']
# 	# EO:
# 	# 1000 --> 100000 --> 10000000 --> None
# 	depts = ['Santa Cr', 'Santa Cruz', 'Cochabam', 'Cochabamba', '', 'Tijuana']
# 	# EO:
# 	# Santa Cruz x2 --> Cochabamba x2 --> n/a x1 --> Tijuana x2
# 	years = ['01', '001', '100', '1001', '1OO2', '2005', '2020', 'Santa Cruz']
# 	# EO:
# 	# 1001 --> 2005 --> 2020

# 	print ("Types:")
# 	print ("############################################################")
# 	for t in types:
# 		print(clean_type(t))

# 	print ("Prices:")
# 	print ("############################################################")
# 	for p in prices:
# 		print(clean_price(p))

# 	print ("Depts:")
# 	print ("############################################################")
# 	for d in depts:
# 		print(clean_dept(d))

# 	print ("Years:")
# 	print ("############################################################")
# 	for y in years:
# 		print(clean_year(y))





