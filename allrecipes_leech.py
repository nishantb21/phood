import requests
import sys

'''
@param recipe id
@return JSON with recipe reviews
'''
def leech(recipeid):
	print(recipeid)
	url = 'https://apps.allrecipes.com/v1/recipes/{}/reviews/'
	headers = {
		'Authorization': 'Bearer 84XAr4Z2Z57+ieH6qwuIreIELMkV8r3bTThXeMCEIvPul4qNGScAVlMMnBYtubd+6quob+PJ14hTpMrHWyL4gkvpaO77IQRILXaivMT11VYAiJquc/3WzdKtZO2HP93a+Pl4j9uPRbuvovewunh4uLO3xhwTu4dESHag0OlqjgssrL7lnP7wfw=='
	}

	response = requests.get(
								url.format(recipeid),
								headers=headers)

	if response.__nonzero__():
		print('GET RecipeID:{:6} {:3} {}\r'.format(recipeid, response.status_code, response.reason))
		return response.json()

	return None

if __name__ == "__main__":
	if len(sys.argv) > 1:
		for recipeid in sys.argv[1:]:
			leech(int(recipeid))
	else:
		leech(25523)