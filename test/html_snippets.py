flat = '''
<div>
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
    <td>1</td><td>2</td><td>3</td><td>4</td>
</tr>
</tbody>
</table>
</div>
'''
