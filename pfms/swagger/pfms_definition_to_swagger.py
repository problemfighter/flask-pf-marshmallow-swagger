from apispec import APISpec
from pfms.swagger.pfms_definition import PFMSDefinition


class PFMSDefinitionToSwagger:

    specification: APISpec

    def __init__(self, specification: APISpec):
        self.specification = specification

    def process(self, definition: PFMSDefinition):
        pass
