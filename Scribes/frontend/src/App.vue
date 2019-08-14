<template>
  <div id="app">
    <NavbarComponent />
      <div class="container">
        <h2>Start Securing the Twittersphere With the Power of the Factom Blockchain! </h2>
      </div>
    <AddAccounts
      @add:twitteraccount="addAccount" />
    
    <account-table 
      :twitteraccounts="twitteraccounts"
      @delete:twitteraccount="deleteAccount" 
      />

    <router-view />
  </div>
</template>

<script>
import NavbarComponent from "@/components/Navbar.vue";
import AddAccounts from "@/components/AddAccounts.vue";
import AccountTable from "@/components/AccountTable.vue";
import { CSRF_TOKEN } from "@/common/csrf_token.js";
import { apiService } from "@/common/api.service.js";

export default {
    name: "App",
    components: {
      NavbarComponent,
      AddAccounts,
      AccountTable,

  },
  data() {
    return {
      twitteraccounts: [],
    }
  },
  methods: {
    async setUserInfo() {
          const data = await apiService("/api/user/");
          const requestUser = data["username"];
          window.localStorage.setItem("username", requestUser);
    },
    async getAccounts() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/twitteraccounts/')
        const data = await response.json()
        this.twitteraccounts = data
      } catch (error) {
        console.error(error)
      }
    },
    async addAccount(twitteraccount) {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/twitteraccounts/', {
          method: 'POST',
          body: JSON.stringify(twitteraccount),
          headers: {
            "content-type": "application/json; charset=UTF-8",
            'X-CSRFTOKEN': CSRF_TOKEN}
        })
        const data = await response.json()
        this.twitteraccounts = [...this.twitteraccounts, data]
      } catch (error) {
        console.error(error)
      }
    },
    async deleteAccount(id) {
      try {
        await fetch(`http://127.0.0.1:8000/api/twitteraccounts/${id}/`, {
          method: 'DELETE',
          headers: {
            "content-type": "application/json; charset=UTF-8",
            'X-CSRFTOKEN': CSRF_TOKEN}
        })
        this.twitteraccounts = this.twitteraccounts.filter(
          twitteraccount => twitteraccount.id !== id
        )
      } catch (error) {
        console.error(error)
      }
    },
    async editAccount(id, updatedAccount) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/twitteraccounts/${id}/`, {
          method: 'PUT',
          body: JSON.stringify(updatedAccount),
          headers: {
            "content-type": "application/json; charset=UTF-8",
            'X-CSRFTOKEN': CSRF_TOKEN}
        })
        const data = await response.json()
        this.twitteraccounts = this.twitteraccounts.map(
          twitteraccount => twitteraccount.id === id ? data : twitteraccount
          )
      } catch (error) {
        console.error(error)
      }
    }
  },
  created() {
    this.getAccounts()
    this.setUserInfo()
  }
}

</script>

<style>
 html, body {
        height: 100%;
        font-family: 'Roboto', sans-serif;
        
    }
h1, h2, h3 {
  text-align: center;
}


</style>
