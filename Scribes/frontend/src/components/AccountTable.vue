<template>
  <div class="container">
        <div id="account-table">
            <p v-if="twitteraccounts.length < 1" class="empty-table">
                No account
            </p>
            <table v-else>
             <thead>
                <tr>
                    <th>Twitter Handle</th>
                    <th>Twitter ID</th>
                    <th>Chain ID</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="twitteraccount in twitteraccounts" :key="twitteraccount.id">
                    <td v-if="editing === twitteraccount.id">
                        <input
                            input type="text"
                            v-model="twitteraccount.handle"
                        />
                    </td>
                    <td v-else>{{ twitteraccount.handle }}</td>

                    <td v-if="editing === twitteraccount.id">
                        <input
                            input type="text"
                            v-model="twitteraccount.twitterid"
                        />
                    </td>
                    <td v-else>{{ twitteraccount.twitterid }}</td>
                    <td> {{ twitteraccount.chainid }} </td>
                    <td v-if="editing === twitteraccount.id">
                        <button
                            class="waves-effect waves-light btn" 
                            @click="editAccount(twitteraccount)"
                            >Save
                            </button>
                        <button 
                            class="muted-button waves-effect waves-light btn" 
                            @click="editing = null"
                            >Cancel
                        </button>
                    </td>
    
                    <td v-else>
                        <button 
                            class="waves-effect waves-light btn"
                            @click="editMode(twitteraccount.id)"
                            > Edit
                        </button>
                        <button 
                            class="waves-effect waves-light btn"
                            @click="$emit('delete:twitteraccount', twitteraccount.id)"
                            > Delete
                        </button>
                    </td>

                </tr>
            </tbody>
            </table>
        </div>
  </div>
</template>

<script>
  export default {
    name: 'AccountTable',
    props: {
        twitteraccounts: Array,
    },
    data() {
        return {
            editing: null,
        }
    },
    methods: {
        editMode(id) {
            this.editing = id
        },

        editAccount(twitteraccount) {
            if (twitteraccount.handle === '' || twitteraccount.twitterid === '') return
            this.$emit('edit:twitteraccount', twitteraccount.id, twitteraccount)
            this.editing = null
        }
    }
  }
</script>

<style scoped>
th, td {
    text-align: center;
}
</style>