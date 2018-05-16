/**
 * The store used for submits
 */
Ext.define('CF.store.SolverConf', {
  extend: 'Ext.data.Store',
  requires: ['CF.model.SolverConf'],
  model: 'CF.model.SolverConf',
  storeId: 'solverConfStore'
});