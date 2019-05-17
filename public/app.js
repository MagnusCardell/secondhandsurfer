const vm = new Vue ({
    el: '#vue-instance',
    data () {
      return {
        baseUrl: 'http://localhost:8005', // API
        searchTerm: '', // search phrase
        searchDebounce: null, // timeout
        searchResults: [], // results
        numHits: 0, // results enumerator
        maxBudget: null,
        filter: false,
        selectedBundle: null,
        hideAll: false,
        swaps: [],
        swaps_raw:[],
        select_i: null,
        select_ii: null
        
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
        this.numHits = response.data.search.length
        this.swaps_raw = response.data.swap
        return response.data.search
      },
      onBudgetInput(){
        this.filter = true;
      },
      showSwapOptions(h, i, inner){
        this.selectedBundle = h;
        this.swaps = this.swaps_raw[inner];
        this.hideAll = true;
        this.select_i = i;
        this.select_ii = inner;
        
      },
      end_swap(){
        this.hideAll = false;
        this.selectedBundle = null;
      },
      swap_this(bund){
        this.selectedBundle = bund;
        this.hideAll = false;
        this.searchResults[this.select_i].data[this.select_ii] = bund;
        this.selectedBundle = null;
      }

    }
  })