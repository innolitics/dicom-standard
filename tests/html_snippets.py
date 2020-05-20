flat = '''
<div>
<a id="flat"></a>
<table frame="box" rules="all">
<thead>
<tr>
    <th>IE</th><th>Module</th><th>Reference</th><th>Usage</th>
</tr>
</thead>
<tbody>
<tr>
    <td>1</td><td>2</td><td>3</td><td>4</td>
</tr>
<tr>
    <td>1</td><td>2</td><td>3</td><td>4</td>
</tr>
<tr>
    <td>1</td><td>2</td><td>3</td><td>4</td>
</tr>
</tbody>
</table>
</div>
'''

with_links = '''
<div>
<a id="with_links"></a>
<table frame="box" rules="all">
<thead>
<tr>
    <th>IE</th><th>Module</th><th>Reference</th><th>Usage</th>
</tr>
</thead>
<tbody>
<tr>
    <td><a href="somelink">1</a></td><td>2</td><td>3</td><td>4</td>
</tr>
<tr>
    <td><a href="somelink">1</a></td><td>2</td><td>3</td><td>4</td>
</tr>
<tr>
    <td><a href="somelink">1</a></td><td>2</td><td>3</td><td>4</td>
</tr>
</tbody>
</table>
</div>

'''

rowspan = '''
<div>
<a id="rowspan"></a>
<table frame="box" rules="all">
<thead>
<tr>
    <th>IE</th><th>Module</th><th>Reference</th><th>Usage</th>
</tr>
</thead>
<tbody>
<tr>
    <td rowspan="3"><a href="somelink">1</a></td><td>2</td><td>3</td><td>4</td>
</tr>
<tr>
    <td>2</td><td>3</td><td>4</td>
</tr>
<tr>
    <td>2</td><td>3</td><td>4</td>
</tr>
</tbody>
</table>
</div>
'''

colspan = '''
<div>
<a id="colspan"></a>
<table frame="box" rules="all">
<thead>
<tr>
    <th>IE</th><th>Module</th><th>Reference</th><th>Usage</th>
</tr>
</thead>
<tbody>
<tr>
    <td colspan="3"><a href="somelink">1</a></td><td>4</td>
</tr>
<tr>
    <td>1</td><td>2</td><td>3</td><td>4</td>
</tr>
<tr>
    <td colspan="3"><a href="somelink">1</a></td><td>4</td>
</tr>
<tr>
    <td>1</td><td>2</td><td>3</td><td>4</td>
</tr>
</tbody>
</table>
</div>
'''

bothspan = '''
<div>
<a id="bothspan"></a>
<table frame="box" rules="all">
<thead>
<tr>
    <th>IE</th><th>Module</th><th>Reference</th><th>Usage</th>
</tr>
</thead>
<tbody>
<tr>
    <td colspan="3" rowspan="2"><a href="somelink">1</a></td><td>4</td>
</tr>
<tr>
    <td>4</td>
</tr>
<tr>
    <td>1</td><td>2</td><td>3</td><td>4</td>
</tr>
</tbody>
</table>
</div>
'''

h3_description = '''
<div class="section">
<div class="section">
<div class="titlepage">
<div>
<div>
<h3 class="title">CT Image IOD Description</h3>
</div>
</div>
</div>
<p>Description</p>
</div>
<div class="section">
<div class="table">
</div>
</div>
</div>
'''

h5_description = '''
<div class="section">
<div class="section">
<div class="titlepage">
<div>
<div>
<h5 class="title">RT Radiation Set IOD Description</h5>
</div>
</div>
</div>
<p>Description</p>
</div>
<div class="section">
<div class="table">
</div>
</div>
</div>
'''

no_description = '''
<div class="section">
<div class="section">
</div>
<div class="section">
<div class="table">
</div>
</div>
</div>
'''
