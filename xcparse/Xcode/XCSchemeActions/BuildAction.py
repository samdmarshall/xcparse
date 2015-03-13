import xml.etree.ElementTree as xml
from ...Helpers import xcrun_helper
from ..PBX import PBXResolver
from .Base_Action import *
from .BuildActionEntry import *

class BuildAction(Base_Action):
    
    def __init__(self, action_xml):
        self.contents = action_xml;
        if 'parallelizeBuildables' in self.contents.keys():
            self.parallel = self.contents.get('parallelizeBuildables');
        if 'buildImplicitDependencies' in self.contents.keys():
            self.implicit = self.contents.get('buildImplicitDependencies');
        self.children = list(map(lambda entry: BuildActionEntry(entry), list(self.contents.find('./BuildActionEntries'))));
        
    def performAction(self, build_system, container, project_constructor, scheme_config_settings):
        for child in self.children:
            project_path = xcrun_helper.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
            project = project_constructor(project_path);
            
            xcrun_helper.perform_xcodebuild(project, container[1].name, 'build', scheme_config_settings);
            
            # target_constructor = PBXResolver(project.objects()[child.target.BlueprintIdentifier]);
            # if target_constructor[0] == True:
            #     target = target_constructor[1](PBXResolver, project.objects()[child.target.BlueprintIdentifier], project, child.target.BlueprintIdentifier);
            #     print target.name;
            #     print '========================';
            #     for phase in target.buildPhases:
            #         phase.performPhase(build_system, target);