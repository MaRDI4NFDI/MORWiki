"""
Types of datasets: Validate and cast them into workable formats
"""

from typing import Annotated, Any, Union
from typing_extensions import Doc
from pydantic import StringConstraints
from pydantic_core import core_schema
from pydantic import BaseModel, GetCoreSchemaHandler, StringConstraints, TypeAdapter
import numpy as np
import scipy.sparse as sp


class Matrix:
    """ Matrix: A numpy array or a scipy sparse matrix. """
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """ Use a simple validator — no pydantic sub-schema for np.ndarray """
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value: Any) -> np.ndarray:
        """
        Validate the input value and convert to manageable datatypes.
        """
        # if value.ndim != 2:
        #     raise ValueError("Expected a 2D float64 matrix")

        if not (isinstance(value, np.ndarray) or sp.issparse(value)):
            raise TypeError("Value must be a numpy ndarray or a scipy sparse matrix")

        if np.issubdtype(value.dtype, np.floating):
            return value.astype(np.float64)

        if np.issubdtype(value.dtype, np.complexfloating):
            return value.astype(np.complex128)

        if np.issubdtype(value.dtype, np.integer):
            return value.astype(np.int64)

        raise TypeError(f"Unsupported dtype: {value.dtype}")


class BaseDataType(BaseModel):
    """ Base class for all data types.
    NOTE: Ignores any additional fields in the data
    """
    model_config = {'extra':'ignore'}


class ABCType(BaseDataType):
    """ Dataset with A, B, and C matrices. """
    A: Matrix
    B: Matrix
    C: Matrix


class ABCDEType(BaseDataType):
    """ Dataset with A, B, C, D, and E matrices. """
    A: Matrix
    B: Matrix
    C: Matrix
    D: Matrix
    E: Matrix


class ABCEType(BaseDataType):
    """ Dataset with A, B, C, and E matrices. """
    A: Matrix
    B: Matrix
    C: Matrix
    E: Matrix


class BCKMType(BaseDataType):
    """ Dataset with B, C, K, and M matrices. """
    B: Matrix
    C: Matrix
    K: Matrix
    M: Matrix

class BCEKMType(BaseDataType):
    """ Dataset with B, C, E, K, and M matrices. """
    B: Matrix
    C: Matrix
    E: Matrix
    K: Matrix
    M: Matrix


DataSet = Union[ABCType, ABCEType, ABCDEType, BCKMType, BCEKMType]
""" Dataset: Union of ABCType, ABCEType, ABCDEType, BCKMType, and BCEKMType. """


DataSetType = TypeAdapter(DataSet)
""" DataSetType: A TypeAdapter for DataSet. """
