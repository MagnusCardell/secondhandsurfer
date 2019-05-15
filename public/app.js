const vm = new Vue ({
    el: '#vue-instance',
    data () {
      return {
        baseUrl: 'http://localhost:8005', // API
        searchTerm: '', // default search term
        searchDebounce: null, // Timeout for search bar debounce
        searchResults: [], // Displayed search results
        numHits: null, // Total search results found
  
        selectedItem: null, // selected object
        paragraphs: [] // Paragraphs being displayed in book preview window
      }
    },
    async created () {
      this.searchResults = await this.search() // Search for default term
    },
    methods: {
      /** Debounce search input by 100 ms */
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