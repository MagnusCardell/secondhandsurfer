const vm = new Vue ({
    el: '#vue-instance',
    data () {
      return {
        baseUrl: 'http://localhost:8005', // API
        searchTerm: '', // search phrase
        searchDebounce: null, // timeout
        searchResults: [], // results
        numHits: null, // results enumerator
  
        selectedBundle: null,
        selectedItem: null, 
      }
    },
    async created () {
      this.searchResults = await this.search() // connection test
    },
    methods: {
      onSearchInput () {
        clearTimeout(this.searchDebounce)
        this.searchDebounce = setTimeout(async () => {
          this.searchResults = await this.search()
        }, 100)
      },
      /** Call API to search for inputted term */
      async search () {
        const response = await axios.post(`${this.baseUrl}/search`, { params: { term: this.searchTerm }, 
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, PUT, OPTIONS, DELETE',
            'Access-Control-Allow-Headers': 'Access-Control-Allow-Methods, Access-Control-Allow-Origin, Origin, Accept, Content-Type',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          } })
        this.numHits = response.data.hits.total
        return response.data.hits.hits
      },

    }
  })