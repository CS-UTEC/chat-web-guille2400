$(function(){
    var url = "/messages";
     $("#grid").dxDataGrid({
         dataSource: DevExpress.data.AspNet.createStore({
             key: "id",
             insertUrl: url,
             updateUrl: url,
             deleteUrl: url,
             loadUrl: url,
             onBeforeSend: function(method, ajaxOptions) {
                 ajaxOptions.xhrFields = { withCredentials: true };
             }
         }),

         editing: {
             allowUpdating: true,
             allowDeleting: true,
             allowAdding: true
         },

         remoteOperations: {
             sorting: true,
             paging: true
         },

         paging: {
             pageSize: 12
         },

         pager: {
             showPageSizeSelector: true,
             allowedPageSizes: [8, 12, 20]
         },

         columns: [{
             dataField: "id",
             dataType: "number",
             allowEditing: true
         }, {
             dataField: "content"
         }, {
             dataField: "sent_on",
             allowEditing: true
         }, {
             dataField: "user_from_id"
         }, {
             dataField: "user_to_id"}]

     }).dxDataGrid("instance");
    });