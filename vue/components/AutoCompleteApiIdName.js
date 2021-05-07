Vue.component('autocompleteapi-idname', {
    template: `
    <div>
        <p>HOLA</p>
        <v-card>ADIOS</v-card>
        <v-autocomplete
            v-model="localValue"
            :items="items"
            :loading="isLoading"
            :search-input.sync="search"
            item-text="name"
            item-value="url"
            :no-data-text="You must select a item"
            hide-selected
            outlined
            persistent-hint
            :label="Select a contact"
            placeholder="Start typing to Search"
            prepend-icon="mdi-database-search"
        ></v-autocomplete>
    </div>
    `,
    props: {
        value: {
            required: true
        }
    },
    data: () => ({
        descriptionLimit: 60,
        entries: [],
        isLoading: false,
        search: null,
        localValue: null
    }),

    computed: {
        items () {
            let r=[]
            this.entries.forEach(entry => r.push({"url": entry.url, "name":this.fullName(entry)}))
            return r
        },
    },
    methods:{
        fullName(entry){
                return `${entry.name} ${entry.surname} ${entry.surname2}`
        },
    },
    watch: {
        search (val) {
            // Items have already been loaded
            if (this.items.length > 0) return

            // Items have already been requested
            if (this.isLoading) return

            this.isLoading = true

            axios.get(`${this.$store.state.apiroot}/api/find/?search=${val}`, this.myheaders())
            .then((response) => {
                this.entries=response.data 
                this.canclick=true;
            }, (error) => {
                this.parseResponseError(error)
                this.canclick=true;
            })
            .finally(() => (this.isLoading = false));
        },
        localValue (newValue) {
            this.$emit('input', newValue)
            console.log(`LocalValue changed and emited input to ${newValue}`)
        },
        value (newValue) {
            this.localValue = newValue
            console.log(`value changed to ${newValue}`)
        }
    },
})
