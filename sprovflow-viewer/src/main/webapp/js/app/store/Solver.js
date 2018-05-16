var solvers = [{
  "abbr": "SPECFEM3D_CARTESIAN_21447",
  "name": "SPECFEM3D_CARTESIAN_21447"
}];

Ext.define('CF.store.Solver', {
  extend: 'Ext.data.Store',
  model: 'CF.model.Solver',
  data: solvers
});