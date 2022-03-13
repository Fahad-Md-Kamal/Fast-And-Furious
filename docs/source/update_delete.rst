=================
DELETE & UPDATE
=================

`Part - Four <https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/5aee14e85069e49b0af141527e5bd24bcda722aa>`_

Delete Item
--------------
Receive item ``ID`` to be deleted. Check if item exist in the data set. If exist delete it and send ``204`` status code. Else raise ``HTTPException`` error. To send related status code add ``status_code=status.HTTP_204_NO_CONTENT`` to the url decorator.

.. code-block:: python
    :emphasize-lines: 3,5

    def find_post_index(id: int):
    """Return Index of the Matching post item"""

    for idx, val in enumerate(my_posts):
        if val['id'] == id:
            return idx

    @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['POST'])
    async def delete_post(id: int):
        """ Delete Post With The Given Id"""

        index = find_post_index(id)
        if index == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not-Found")

        my_posts.pop(index)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

Update Item
--------------

Receive Item ``id`` to be updated. Check if the item exists. If exists get the index of the item. Convert the payload data to dict. Assign the given ID to the dict. Replace the Item to the index position of the list.


.. code-block:: python
    :emphasize-lines: 1, 8

    def find_post_index(id: int):
        """Return Index of the Matching post item."""

        for idx, val in enumerate(my_posts):
            if val['id'] == id:
                return idx

    @app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
    async def update_post(id: int, post: Post):
        """Update a Post with the payload"""

        index = find_post_index(id)
        if index == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not-Found")
                
        post_dict = post.dict()
        post_dict['id'] = id
        my_posts[index] = post_dict
        return {"message": post_dict}
