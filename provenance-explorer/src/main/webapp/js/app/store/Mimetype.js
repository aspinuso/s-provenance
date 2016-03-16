var mimetypes = [{
  "mime": "application/octet-stream",
  "desc": ""
}, {
  "mime": "image/png",
  "desc": ""
}, {
  "mime": "video/mpeg",
  "desc": ""
}]

var mimetypesStore = Ext.define('CF.store.Mimetype', {
  extend: 'Ext.data.Store',
  model: 'CF.model.Mimetype',
  data: mimetypes
});