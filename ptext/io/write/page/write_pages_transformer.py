#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of \Type \Pages
"""
import logging
import typing
from typing import Optional

from ptext.io.read.types import (
    AnyPDFType,
    Dictionary,
    Reference,
    Name,
)
from ptext.io.write.object.write_dictionary_transformer import (
    WriteDictionaryTransformer,
)
from ptext.io.write.write_base_transformer import (
    WriteTransformerContext,
)

logger = logging.getLogger(__name__)


class WritePagesTransformer(WriteDictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of \Type \Pages
    """

    def __init__(self):
        self.queue: typing.List[AnyPDFType] = []

    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Dictionary) and "Type" in any and any["Type"] == "Pages"

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert isinstance(object_to_transform, Dictionary)
        assert context is not None

        # \Kids can be written immediately
        object_to_transform[Name("Kids")].set_can_be_referenced(False)

        # queue writing of \Page objects
        queue: typing.List[AnyPDFType] = []
        for i, p in enumerate(object_to_transform["Kids"]):
            queue.append(p)
            ref: Reference = self.get_reference(p, context)
            object_to_transform["Kids"][i] = ref

        # delegate to super
        super(WritePagesTransformer, self).transform(object_to_transform, context)

        # write \Page objects
        for p in queue:
            self.get_root_transformer().transform(p, context)