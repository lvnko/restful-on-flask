[回到目錄](overview.md) | [上一章](04-api-perf-index.md)
---
## 5. 不同網站 Session 部署之優缺
<table>
  <thead>
    <tr>
        <th>種類</th>
        <th>優點 (Pros)</th>
        <th>缺點 (Cons)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan=3>客戶端 Session (Client-side Session)</td>
      <td>Low latency. Validating and creating sessions is fast as it doesn't need to hit the data-store</td>
      <td>Session can't revoke immediately.</td>
    </tr>
    <tr>
      <td>No state to manage on servers</td>
      <td>Cookie size is greater</td>
    </tr>
    <tr>
      <td>New web server can be added instantly</td>
      <td>User details are exposed</td>
    </tr>
    <tr>
      <td rowspan=4>伺服器端 Session (Server-side Session)</td>
      <td>Can revoke a session instantly.</td>
      <td>Replication has a performance cost and increases complexity.</td>
    </tr>
    <tr>
      <td>Cookie size is smaller.</td>
      <td>A central store will limit scaling and increase latency.</td>
    </tr>
    <tr>
      <td>User details are not exposed</td>
      <td rowspan=2>Confining users to a specific server leads to problems when that server needs to come down</td>
    </tr>
    <tr>
      <td>Replicate that session data across all of the web servers</td>
    </tr>
  </tbody>
</table>
