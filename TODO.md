# Phractal
The following tasks are WIP.

## Packaging
- [x] Sort out setup.py

## Testing
- [x] Write tests
- [x] Automate tests for new git pushes

## Deployment
- [x] Fix the DANG image... why is my absolute URL not working on test.pypi.org??
- [x] Squash commits to date... again
- [ ] Undeploy and re-deploy to sort out that pesky versioning issue where the only difference is the readme image
- [ ] Check that branch protection works
- [ ] set up CI Github Action for Pypi deploy on main branch pull req. approval 
  - [ ] build in a check to make sure that the deploying version number has been incremented from the currently deployed version

## Development
- [ ] Need to find a way to prevent a user from using a banned variable name in a template (i.e. `template`!)
- [ ] Need to get ValidatedCachedProperty working with parameterized generics in typehints -> https://lyz-code.github.io/blue-book/coding/python/pydantic_types/#generic-classes-as-types
- [ ] A method that wraps the output in html boilerplate
- [ ] HTML boilerplate for printable media