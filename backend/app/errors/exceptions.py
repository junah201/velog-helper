from fastapi import HTTPException


class NotFoundBlog(HTTPException):
    def __init__(self, blog_id: str = None):
        super().__init__(
            status_code=404,
            detail=f"Not Found Blog ID : {blog_id}",
        )


class NotFoundUser(HTTPException):
    def __init__(self, user_id: str = None):
        super().__init__(
            status_code=404,
            detail=f"Not Found User ID : {user_id}",
        )


class AlreadyBookmarkedBlog(HTTPException):
    def __init__(self, user_id: str = None, blog_id: str = None):
        super().__init__(
            status_code=403,
            detail=f"User ID : {user_id} already Bookmarked Blog ID : {blog_id}",
        )


class NotBookmarkedBlog(HTTPException):
    def __init__(self, user_id: str = None, blog_id: str = None):
        super().__init__(
            status_code=403,
            detail=f"User ID : {user_id} Not Bookmarked Blog ID : {blog_id}",
        )


class AlreadyRegistedUser(HTTPException):
    def __init__(self, user_id: str = None):
        super().__init__(
            status_code=405,
            detail=f"User ID : {user_id} Is Already Registed",
        )


class NotFoundBookmark(HTTPException):
    def __init__(self, user_id: str = None, blog_id: str = None):
        super().__init__(
            status_code=405,
            detail=f"User ID : {user_id} Is not bookmark Blog ID : {blog_id}",
        )
