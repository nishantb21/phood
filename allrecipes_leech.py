import requests
import sys
import json
import os
import urllib


def has_next_page(responsejson):
  return responsejson['links'].__contains__("next")


'''
@param recipe id
@return JSON with recipe reviews
'''


def leech(recipeid):
  url = 'https://apps.allrecipes.com/v1/recipes/{}/reviews/'
  headers = {
      'Authorization': 'Bearer 84XAr4Z2Z57+ieH6qwuIreIELMkV8r3bTThXeMCEIvPul4qNGScAVlMMnBYtubd+6quob+PJ14hTpMrHWyL4gkvpaO77IQRILXaivMT11VYAiJquc/3WzdKtZO2HP93a+Pl4j9uPRbuvovewunh4uLO3xhwTu4dESHag0OlqjgssrL7lnP7wfw=='
  }
  queryparams = {
      "pagesize": 100,
      "page": 1
  }

  response = requests.get(
      url.format(recipeid),
      headers=headers,
      params=queryparams)
  responsejson = response.json()

  print(
      'GET Recipe ID:{:6} Page {:2} - {:3} {}'.format(
          recipeid, 1, response.status_code, response.reason),
      end='\r')

  reviews = list()

  while has_next_page(responsejson):
    pageno = int(
        urllib.parse.parse_qs(
            urllib.parse.urlparse(
                responsejson["links"]["next"]["href"]).query)['page'][0])
    print('GET Recipe ID:{:6} Page {:2} - {:3} {}'.format(
        recipeid, pageno, response.status_code, response.reason), end='\r')

    reviews.extend(responsejson["reviews"])
    queryparams["page"] = pageno
    response = requests.get(
        url.format(recipeid),
        headers=headers,
        params=queryparams)

    responsejson = response.json()

  reviews.extend(responsejson["reviews"])

  if not os.path.exists("recipereviews"):
    os.mkdir("recipereviews")

  with open(
          os.path.join("recipereviews", "{}.json".format(recipeid)),
          "w") as outfile:
    json.dump(reviews, outfile, indent='\t')

  print("~ Recipe ID {:6}: Wrote {:4} reviews ~".format(
      recipeid, len(reviews)))

  return reviews


if __name__ == "__main__":
  if len(sys.argv) > 1:
    for recipeid in sys.argv[1:]:
      leech(int(recipeid))
  else:
    leech(68461)
