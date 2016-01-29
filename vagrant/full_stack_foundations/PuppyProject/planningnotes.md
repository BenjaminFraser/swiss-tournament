# Structure of The Goody Basket

- A main introduction page, describing the features of the site and linking to the main pages, such as login, category list, etc. 
- A category list, with the ability to view, edit and delete a category, along with an ability to add a new item to the database. 
- To add a new item to a category, a user must be logged in.
- To edit or delete an item, the original user must be the one logged in.

## Views

'''

    /views
    ├── introPage
    ├── showCategories
    ├── categoryItems
    ├── createCategory
    ├── editCategory
    ├── deleteCategory
    ├── newCategoryItem
    ├── editCategoryItem
    ├── deleteCategoryItem
    ├── login
