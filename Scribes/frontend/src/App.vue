<template>
  <div id="app">
    <NavbarComponent />
    <h1>Add An Account</h1>
    <AddAccounts
      @add:twitteraccount="addAccount" />
    
    <h2>Your Tracked Accounts</h2>
    <account-table 
      :twitteraccounts="twitteraccounts"
      @delete:twitteraccount="deleteAccount" 
      @edit:twitteraccount="editAccount"/>

    <router-view />
  </div>
</template>

<script>
import NavbarComponent from "@/components/Navbar.vue";
import AddAccounts from "@/components/AddAccounts.vue";
import AccountTable from "@/components/AccountTable.vue";

export default {
    name: "App",
    components: {
      NavbarComponent,
      AddAccounts,
      AccountTable

  },
  data() {
    return {
      twitteraccounts: [
        {
          id: 1,
          handle: 'factombot',
          twitterid: '11234',
        },
        {
          id: 2,
          handle: 'realdonaldtrump',
          twitterid: '3948756',
        },
        {
          id: 3,
          handle: 'fct_bot',
          twitterid: '837987989',
        },
      ],
    }
  },
  methods: {
    addAccount(twitteraccount) {
      const lastId =
        this.twitteraccounts.length > 0
          ? this.twitteraccounts[this.twitteraccounts.length - 1].id
          : 0;
      const id = lastId + 1;
      const newAccount = { ...twitteraccount, id };

      this.twitteraccounts = [...this.twitteraccounts, twitteraccount]
    },
    deleteAccount(id) {
      this.twitteraccounts = this.twitteraccounts.filter(
        twitteraccount => twitteraccount.id !== id
      )
    },
    editAccount(id, updatedAccount) {
      this.twitteraccounts = this.twitteraccounts.map(twitteraccount =>
        twitteraccount.id === id ? updatedAccount : twitteraccount)
    }
  }
}

</script>

<style>
 html, body {
        height: 100%;
        font-family: 'Roboto', sans-serif;
        
    }
h1, h2 {
  text-align: center;
}
</style>
