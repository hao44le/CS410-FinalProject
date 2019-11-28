import React, { Component } from 'react';
import {
  ReactiveBase,
  DataSearch,
  MultiList,
  RangeSlider,
  SingleRange,
  SelectedFilters,
  ResultCard,
  ReactiveList,
} from '@appbaseio/reactivesearch';
import './App.css';

class K12 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: false,
    };
  }

  toggleState = () => {
    const { visible } = this.state;
    this.setState({
      visible: !visible,
    });
  };

  render() {
    return (
      <ReactiveBase
        app="chinesek12_wechat_article"
        url="https://search-chinesek12-sp2avv7lleofzv5qu5m6qkk4by.us-east-2.es.amazonaws.com/"
      >
        <div className="navbar">
          <div className="logo">
            Chinese K12<b> Wechat Article </b>Search Engine
          </div>
          <DataSearch
            className="datasearch"
            componentId="mainSearch"
            dataField={[
              'title',
              'title.search',
              'title.autosuggest',
              'wechat_name',
              'wechat_name.search',
              'wechat_name.autosuggest'
            ]}
            queryFormat="and"
            placeholder="Search for a article title or wechat account name"
            innerClass={{
              input: 'searchbox',
              list: 'suggestionlist',
            }}
            autosuggest={false}
            iconPosition="left"
            filterLabel="search"
          />
        </div>
        <div className="display">
          <div className={`leftSidebar ${this.state.visible ? 'active' : ''}`}>
          </div>
          <div className="mainBar">
            <SelectedFilters />
            <ReactiveList
              componentId="results"
              dataField="title"
              react={{
                and: [
                  'mainSearch',
                  // 'wechatTypeFilter',
                  // 'publishFilter',
                  // 'authorFilter',
                ],
              }}
              pagination
              size={12}
              sortOptions={[
                {
                  dataField: 'reads',
                  sortBy: 'desc',
                  label: 'Reads (High to low)',
                },
                {
                  dataField: 'publish_time',
                  sortBy: 'desc',
                  label: 'Publish Time (Recent to Remote)',
                },
              ]}
              render={({ data }) => (
                <ReactiveList.ResultCardsWrapper>
                  {data.map(item => (
                    <ResultCard href={item.link} key={item._id}>
                      <ResultCard.Description
                        dangerouslySetInnerHTML={{
                          __html:
                            `<h2><div class='result-title'>${item.title}</div></h2>` +
                            `<div class='result-author' title='${
                              item.wechat_name
                            }'>Created by <span class="star">${item.wechat_name}</span></div>`
                            + `<div>Wechat ID: <span class="star">${item.wechat_ID}</span></div>`
                            + `<div>Publish Time: <span class="star">${(new Date(Date.parse(item.publish_time))).toDateString()}</span></div>`
                            + `<div>Publish Location: <span class="star">${item.location}</span></div>`
                            + `<div>Reads: <span class="star">${item.reads}</span></div>`
                            + `<div>Likes: <span class="star">${item.likes}</span></div>`
                            + `<div>Comments: <span class="star">${item.comments}</span></div>`,
                        }}
                      />
                    </ResultCard>
                  ))}
                </ReactiveList.ResultCardsWrapper>
              )}
              className="result-data"
              innerClass={{
                title: 'result-title',
                listItem: 'result-item',
              }}
            />
          </div>
          <div
            role="button"
            tabIndex="0"
            onKeyPress={this.toggleState}
            onClick={this.toggleState}
            className={`toggle-btn ${this.state.visible ? 'active' : ''}`}
          >
            {this.state.visible ? '📚  Show Articles' : '📂  Show Filters'}
          </div>
        </div>
      </ReactiveBase>
    );
  }
}

export default K12;
