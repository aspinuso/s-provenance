var modes = [{
  "mode": "OR"
}, {
  "mode": "AND"
}]

var modeStore = Ext.define('CF.store.ModeStore', {
  extend: 'Ext.data.Store',
  model: 'CF.model.Mode',
  data: modes
});