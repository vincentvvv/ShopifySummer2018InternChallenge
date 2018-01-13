import urllib2
import simplejson
import json
from collections import OrderedDict

"""
Vincent Vuong
Shopify Summer 2018 Internship application
"""

"""
- BASE_URL to query the API, Requires a page id and a page #
- PAGE_ID depending on the challenge please set to one of [1, 2]
"""
BASE_URL = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id={}&page={}"
PAGE_ID = 1

"""
- Menu Class
  deserializes the json query for a menu item
"""
class Menu:
    def __init__(self, id, data, child_ids, parent_id = None):
        self.id = id
        self.data = data
        self.child_ids = child_ids
        self.parent_id = parent_id

	def __init__(self, **entries):
		self.__dict__.update(entries)

    def __str__(self):
        return "{id: %s, data: %s, child_ids: %s, parent_id: %s" % (self.id, self.data, self.child_ids, self.parent_id)

"""
Makes calls to the API to fetch the menu items. Places the items in menuItems and rootMenuItems (if it does not have a parent_id)
"""
def fetchMenuItems(rootMenuItems, menuItems):
	pageNumber = 1

	while(True):
		response = urllib2.urlopen(BASE_URL.format(PAGE_ID, pageNumber))
		data = simplejson.load(response)

		if len(data['menus']) == 0:
			break

		for menu in data['menus']:
			menuItem = Menu(**menu)
			menuItems[menuItem.id] = menuItem
			if not menuItem.parent_id:
				rootMenuItems.append(menuItem)

		pageNumber += 1

"""
Goes through a visited dictionary to get the visited nodes.
"""
def getChildren(visited, root):
	children = []

	for key, value in visited.items():
		if value and key != root:
			children.append(key)

	return children

"""
Returns True if a given menu node has a cycle
"""
def hasCycle(menu, menuItems, visited, recStack):
	visited[menu.id] = True
	recStack[menu.id] = True

	for child_id in menu.child_ids:
		if visited[child_id] == False:
			if hasCycle(menuItems[child_id], menuItems, visited, recStack) == True:
				return True
		elif recStack[child_id] == True:
			return True

	return False

"""
Format a given id and childrens into a ordered dictionary
"""
def formatItem(id, children):
	item = OrderedDict()
	item["root_id"] = id
	item["children"] = children
	return item

"""
Checks that rootMenuItems are either valid menu items or invalid menu items
"""
def validate(rootMenuItems, menuItems):
	result = OrderedDict()
	result["valid_menus"] = [] 
	result["invalid_menus"] = []

	for root in rootMenuItems:
		visited = {}
		for key, value in menuItems.items():
			visited[key] = False

		if hasCycle(root, menuItems, visited, visited):
			result["invalid_menus"].append(formatItem(root.id, getChildren(visited, -1)))
		else:
			result["valid_menus"].append(formatItem(root.id, getChildren(visited, root.id)))

	return json.dumps(result)

"""
Returns a Json result of valid_menus and invalid_menus
"""
def validateMenus():
	rootMenuItems = []
	menuItems = {}

	fetchMenuItems(rootMenuItems, menuItems)
	return validate(rootMenuItems, menuItems)

###############################################################################
###############################################################################

solution = validateMenus()
print(repr(solution))