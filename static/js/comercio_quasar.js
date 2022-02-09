axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

const endpoint = 'http://127.0.0.1:8000/'
// const endpoint = `${process.env.APIURL}`

/*
  Example kicking off the UI. Obviously, adapt this to your specific needs.
  Assumes you have a <div id="q-app"></div> in your <body> above
 */
new Vue({
    el: '#q-app',
    delimiters: ['${', '}'],
    data: {
        url: process.env.VUE_APP_URL,
        filter: '',
        comercios: [],
        columns: [
            {
                name: 'id',
                required: true,
                label: 'ID',
                align: 'left',
                field: row => row.value,
                format: val => `${val}`,
                style: 'width: 500px',
                classes: 'my-special-class',
                headerStyle: 'width: 500px',
                headerClasses: 'my-special-class',
                sortable: true
            },
            {
                name: 'description',
                align: 'left',
                label: 'Descrição',
                field: 'description',
                sortable: true
            }
        ]
    },
    mounted() {
        axios.get(endpoint + 'api/comercios/')
        .then( (response) => {
                this.comercios = response.data.data;
            }
        )
    },
    methods: {},
})
