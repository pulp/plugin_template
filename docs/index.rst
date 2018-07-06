Plugin_Template Documentation
=============================

These documents divided into two type:

1. Plugin Template Documentation explains how to use the template, how to expand a bootstrapped
   plugin into a fully functional plugin. These docs also discuss moving forward with complete
   plugins, includng how to release, generate a CLI/bindings, and presents standard options for
   issue trackng, host docs, etc. All of these documents will be in the plugin-writer directory.

2. Plugin Documentation framework is a set of docs that are intended to be included (with renaming)
   in the bootstrapping of plugins. These docs create a skeleton for plugins, making documenting a
   plugin simpler and encouraging documentation patterns between plugins (so users can switch
   between them easily). This section will include installation, workflows, and anything that most
   plugins should include. All documents outside of the plugin-writer directory are templated
   docuements for each plugin.

Outline
=======

The outline is an overview of what the documentation *will be* and is the high level planning
document for this work.

## Purpose

The purpose of these docs is to guide a plugin writer through the entire process of creating a
plugin. The docs should strive to be *completely* comprehensive, explicitly stating assumed
knowledge or providing links to prerequisite documentation.

## Introduction

- link to "what plugins do" in pulpcore documentation
- other useful links
- 10,000 ft overview of the process
  - link to overview documentation in pulpcore
  - use template to bootstrap
  - creation of custom subclasses to define plugin models, viewsets, serializers, tasks, and stages


## README

Brief explanation of the template,

- link to rst documentation index
- Walkthrough use of bootstrap.py.
- provide basic "sanity check" documentation:
  - should be able to sync (no units created, but task will complete)
  - should be able to publish (no units published, but task will complete)
  - pulp-smash tests?

## Walkthrough

- Prereqs, link to introduction
- Plan plugin, link
- bootstrap plugin, link
- Discoverability, tldr & link
- Custom classes
  - Explain models, viewsets, serializers, tasks, stages
  - Link to a .py file for each
    - .py contains simple working versions of each
    - also contains detailed comments explaining what the code does
    - also contains commented out code to serve as an example for idiomatic use
    - For each class to be implemented, document (in the walkthrough) how to test that the class
        has been created correctly with httpie calls


## Reference

This section will contain more detailed explanations of complex topics glossed in the walkthrough.
- Discoverability
- Error handling
- Documentation docs
THis section also contains advanced usage that is not mentioned in the walkthrough.
- CLI
- Live API
- Releasing

## Template

TODO: add this directory to bootstrap.py

This section will contain a skeleton for the new plugin's docs (not plugin writer docs)
- Installation
- Release notes
- Workflows
- Index
- docs conf and Makefile

