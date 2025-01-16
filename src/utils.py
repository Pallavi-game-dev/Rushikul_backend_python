

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

def getResponse(is_success, data=None, message=None):
    if is_success:
        data = data if data else []
        final_message = "Successfully" if data else "Data not Found"
        response_data = dict(
            status="success", message=final_message, data=data, api_message=message)
        response_data =jsonable_encoder(response_data)
        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

    else:
        if not message:
            message = "Something went Wrong"

        response_dict = dict(status="failure", message=message, data=data)
        response_data = jsonable_encoder(response_dict)

        return JSONResponse(
            content=response_data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )