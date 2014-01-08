def get_subdomain(request):
	try:
		subdomain = request.META['HTTP_HOST'].split('.')[0]
		subdomain = subdomain.upper()
	except:
		subdomain = ''
	return subdomain
