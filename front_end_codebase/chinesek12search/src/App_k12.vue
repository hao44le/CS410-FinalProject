<template>
  <div id="app">
    <ReactiveBase
      app="chinesek12_wechat_article"
      url="https://search-chinesek12-sp2avv7lleofzv5qu5m6qkk4by.us-east-2.es.amazonaws.com"
    >
      <div class="navbar">
        <h2><span class="logo">Chinese K12 Wechat Article</span>Search</h2>
        <DataSearch
          componentId="title"
          iconPosition="right"
          :dataField="[
            'title',
            'title.search',
            'title.autosuggest'
          ]"
          className="data-search"
          :showClear="false"
          placeholder="Search for Chinese K12 Wechat Articles"
        />
      </div>
      <button class="toggle" @click="switchContainer">
        {{ showArticles ? "Show Filters 💣" : "Show Articles 📚" }}
      </button>
      <div class="container">
        <div class="filters-container" :class="{ full: !showArticles }">
          <!-- <MultiList
            componentId="Authors"
            dataField="authors.raw"
            class="filter"
            title="Select Authors"
            selectAllLabel="All Authors"
            :react="{ and: ['Ratings', 'title'] }"
          />
          <SingleRange
            componentId="Ratings"
            dataField="average_rating"
            :data="[
              { start: 0, end: 3, label: 'Rating < 3' },
              { start: 3, end: 4, label: 'Rating 3 to 4' },
              { start: 4, end: 5, label: 'Rating > 4' }
            ]"
            title="Book Ratings"
            class="filter"
          /> -->
        </div>

        <ReactiveList
          componentId="SearchResult"
          dataField="original_title.raw"
          :class="{ full: showArticles }"
          :pagination="true"
          :from="0"
          :size="8"
          :showResultStats="true"
          className="result-list-container"
          :innerClass="{ list: 'books-container', poweredBy: 'appbase' }"
        >

          <div slot="renderItem" class="book-content" slot-scope="{ item }">
            <a
              key="item._id"
              target="_blank"
              :href="

                  item.link
              "
            >
              <div class="image">
                <img :src="item.image" alt="Book Cover" class="book-image" />
                <div class="rating">{{ item.average_rating_rounded }} ⭐️</div>
                <div class="details">
                  <h4 class="book-header">{{ item.original_title }}</h4>
                  <p>By {{ item.authors }}</p>
                </div>
              </div>
            </a>
          </div>
        </ReactiveList>
      </div>
    </ReactiveBase>
  </div>
</template>

<script>
import "./styles.css";

export default {
  name: "app",
  data: function() {
    return {
      showArticles: window.innerWidth <= 768 ? true : false
    };
  },
  methods: {
    switchContainer: function() {
      return (this.showArticles = !this.showArticles);
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
