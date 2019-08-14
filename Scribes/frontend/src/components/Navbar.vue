
<template>
 
  <div>
        <md-toolbar class="md-accent" md-elevation="1">
            <router-link
                :to="{ name: 'home' }"
                class="md-title"
                style="flex: 1"
                >Scribe
            </router-link>
        <md-menu md-direction="bottom-end">
            <md-button class="md-icon-button" md-menu-trigger>
                <md-icon>settings</md-icon>
            </md-button>
            <md-menu-content>
                <md-menu-item>
                    <router-link
                        :to="{ name: 'home' }"
                        class="button-text"
                        >Home
                    </router-link>
                </md-menu-item>
                <md-menu-item>
                    <a  class="button-text" href="/accounts/logout/">Logout</a>
                </md-menu-item>
            </md-menu-content>
        </md-menu>
        <md-badge md-content="1">
            <md-button class="md-icon-button">
                <md-icon>notifications</md-icon>
            </md-button>
        </md-badge>
        </md-toolbar>
  </div>
 
</template>


<script>
export default {
    name: "NavbarComponent"
}
</script>


<style>
.button-text {
    color: white;
}
.md-toolbar {
  background-color: #29b6f6  !important;
}
.md-button {
  color: white;
}
.md-menu-item {
    background-color: #29b6f6;
}
.md-title {
    font-weight: bold;
    font-size: 130%;
    color: white;
}
.md-title:hover {
    color: #f56f12 !important;
}
.md-menu-content {
    background-color: #29b6f6;
}
</style>
