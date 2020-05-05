from gaphor.core.modeling.properties import (
    association,
    attribute,
    relation_many,
    relation_one,
)
from gaphor.UML import (
    Abstraction,
    AcceptEventAction,
    ActivityEdge,
    ActivityPartition,
    Behavior,
    Class,
    Classifier,
    Comment,
    Connector,
    ConnectorEnd,
    DataType,
    Dependency,
    DirectedRelationship,
    Element,
    Feature,
    Generalization,
    InstanceSpecification,
    InvocationAction,
    NamedElement,
    ObjectNode,
    Operation,
    Optional,
    Parameter,
    Port,
    Property,
    StructuralFeature,
    Trigger,
)


class AbstractRequirement(NamedElement):
    verifiedBy: attribute[NamedElement]
    master: attribute[AbstractRequirement]
    refinedBy: attribute[NamedElement]
    satisfiedBy: attribute[NamedElement]
    base_NamedElement: attribute[NamedElement]
    text: attribute[str]
    derived: attribute[AbstractRequirement]
    tracedTo: attribute[NamedElement]
    id: attribute[str]


class AcceptChangeStructuralFeatureEventAction(AcceptEventAction):
    pass


class ElementPropertyPath:
    pass


class AddStructuralFeatureValueAction:
    pass


class AddFlowPropertyValueOnNestedPortAction(
    ElementPropertyPath, AddStructuralFeatureValueAction
):
    pass


class AdjuntProperty(Property):
    principal: relation_one[None]


class DirectedRelationshipPropertyPath(DirectedRelationship):
    sourceContext: relation_one[None]
    targetContext: relation_one[None]


class Allocate(DirectedRelationshipPropertyPath, Abstraction):
    pass


class AllocateActivityPartition(ActivityPartition):
    pass


class BindingConnector(Connector):
    pass


class Block(Class):
    isEncapsulated: attribute[int]


class EndPathMultiplicity(Property):
    upper: attribute[int]
    lower: attribute[int]


class BoundReference(EndPathMultiplicity):
    bindingPath: attribute[Property]
    boundend: attribute[ConnectorEnd]


class ChangeEvent:
    pass


class ChangeSructuralFeatureEvent(ChangeEvent):
    structuralFeature: relation_one[None]


class ClassifierBehaviorProperty:
    pass


class ClassifierBehaviorProperty(Property):
    pass


class Conform(Generalization):
    pass


class ConnectorProperty(Property):
    connector: attribute[Connector]


class ConstraintBlock(Block):
    pass


class Rate(ActivityEdge, Parameter):
    rate: attribute[InstanceSpecification]


class Continuous(Rate):
    pass


class ControlOperator(Behavior, Operation):
    pass


class Trace:
    pass


class Trace(DirectedRelationshipPropertyPath, Trace):
    pass


class Copy(Trace):
    pass


class DeriveReqt(Trace):
    pass


class DirectedFeature(Feature):
    featureDirection: attribute[None]


class Discrete(Rate):
    pass


class DistributedProperty(Property):
    pass


class ElementGroup(Comment):
    member: attribute[Element]
    name: attribute[str]
    orderedMember: attribute[Element]
    size: attribute[int]
    criterion: attribute[str]


class ElementPropertyPath(Element):
    propertyPath: relation_many[None]


class ElementPropertyPath:
    pass


class Expose(Dependency):
    pass


class FlowProperty(Property):
    direction: attribute[None]


class FullPort(Port):
    pass


class InterfaceBlock(Block):
    pass


class InvocationOnNestedPortAction(ElementPropertyPath, InvocationAction):
    onNestedPort: relation_many[None]


class NestedConnectorEnd(ElementPropertyPath, ConnectorEnd):
    pass


class NoBuffer(ObjectNode):
    pass


class Overwrite(ObjectNode):
    pass


class ParameterSet:
    pass


class ParticipantProperty(Property):
    end: attribute[Property]


class Probability(ParameterSet, ActivityEdge):
    probability: attribute[ValueSpecification]


class Problem(Comment):
    pass


class PropertySpecificType(Classifier):
    pass


class ProxyPort(Port):
    pass


class Rationale(Comment):
    pass


class Refine:
    pass


class Refine(DirectedRelationshipPropertyPath, Refine):
    pass


class Requirement(AbstractRequirement, Class):
    pass


class Satisfy(Trace):
    pass


class Stakeholder(Classifier):
    concernList: attribute[Comment]
    concern: attribute[str]


class Tagged(Property):
    nonunique: attribute[bool]
    subsets: attribute[str]
    ordered: attribute[bool]


class TestCase(Behavior, Operation):
    pass


class TriggerOnNestedPort(ElementPropertyPath, Trigger):
    onNestedPort: relation_many[None]


class ValueType(DataType):
    unit: relation_one[None]


class Verify(Trace):
    pass


class View(Class):
    stakeholder: attribute[Stakeholder]
    viewpoint: attribute[Viewpoint]


class Viewpoint(Class):
    concern: attribute[str]
    purpose: attribute[str]
    concernList: attribute[Comment]
    stakeholder: attribute[Stakeholder]
    language: attribute[str]
    method: attribute[Behavior]
    presentation: attribute[str]
