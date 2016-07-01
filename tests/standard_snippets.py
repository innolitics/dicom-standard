macro_caller = '''
                <div class="table">
                <a id="calling_table"></a>
                <p class="title">Calling Table</p>
                <div class="table-contents">
                <table frame="box" rules="all">
                <thead>
                </thead>
                <tbody>
                    <tr>
                    <td><p><span>Include <a href="https://somelink.com/thispage.html#macro"></a></span></p></td>
                    </tr>
                </tbody>
                </table>
                </div>
                </div>
                '''

macro_callee = '''
                <div class="table">
                <a id="macro"></a>
                <p class="title">Called Table</p>
                <div class="table-contents">
                <table frame="box" rules="all">
                <thead>
                </thead>
                <tbody>
                    <tr>
                    <td>Useful Information</td>
                    </tr>
                </tbody>
                </table>
                </div>
                </div>
               '''

divlist = '''
                <div class="table">
                <a id="tbl1"></a>
                <p class="title">tbl1</p>
                <div class="table-contents">
                <table frame="box" rules="all">
                <thead>
                </thead>
                <tbody>
                    <tr>
                    <td>Useful Information</td>
                    </tr>
                </tbody>
                </table>
                </div>
                </div>
                <div class="table">
                <a id="tbl2"></a>
                <p class="title">tbl2</p>
                <div class="table-contents">
                <table frame="box" rules="all">
                <thead>
                </thead>
                <tbody>
                    <tr>
                    <td>Useful Information</td>
                    </tr>
                </tbody>
                </table>
                </div>
                </div>
                <div class="table">
                <a id="tbl3"></a>
                <p class="title">tbl3</p>
                <div class="table-contents">
                <table frame="box" rules="all">
                <thead>
                </thead>
                <tbody>
                    <tr>
                    <td>Useful Information</td>
                    </tr>
                </tbody>
                </table>
                </div>
                </div>
               '''

cr_iod_section = '''
            <div class="section">
               <div class="titlepage">
                  <div>
                     <div>
                        <h2 class="title" style="clear: both">
                           <a id="sect_A.2" shape="rect"></a>A.2&nbsp;Computed Radiography Image IOD</h2>
                     </div>
                  </div>
               </div>
               <div class="section">
                  <div class="titlepage">
                     <div>
                        <div>
                           <h3 class="title">
                              <a id="sect_A.2.1" shape="rect"></a>A.2.1&nbsp;CR Image IOD Description</h3>
                        </div>
                     </div>
                  </div>
                  <p>
                     <a id="para_d1de8bb0-9b4c-4318-839e-e466a8e3de2e" shape="rect"></a>The Computed Radiography (CR) Image Information Object Definition specifies an image that has been created by a computed radiography imaging device.</p>
                  <div class="note" style="margin-left: 0.5in; margin-right: 0.5in;">
                     <h3 class="title">Note</h3>
                     <p>
                        <a id="para_f15c3af6-cfd3-4764-ba54-1674fe6f3602" shape="rect"></a>Digital Luminescence Radiography is an equivalent term for computed Radiography.</p>
                  </div>
               </div>
               <div class="section">
                  <div class="titlepage">
                     <div>
                        <div>
                           <h3 class="title">
                              <a id="sect_A.2.2" shape="rect"></a>A.2.2&nbsp;CR Image IOD Entity-Relationship Model</h3>
                        </div>
                     </div>
                  </div>
                  <p>
                     <a id="para_6bd914ca-bef5-40d6-92c7-dbe9e8f34759" shape="rect"></a>This IOD uses the E-R Model in <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_A.1.2" title="A.1.2 IOD Entity-Relationship Model" shape="rect">Section&nbsp;A.1.2</a>, with only the Image IE below the Series IE. The Frame of Reference IE is not a component of this IOD.</p>
               </div>
               <div class="section">
                  <div class="titlepage">
                     <div>
                        <div>
                           <h3 class="title">
                              <a id="sect_A.2.3" shape="rect"></a>A.2.3&nbsp;CR Image IOD Module Table</h3>
                        </div>
                     </div>
                  </div>
                  <p>
                     <a id="para_8e9b9882-30e4-4395-9774-eab5ea4559e8" shape="rect"></a>
                     <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.2-1" title="Table A.2-1. CR Image IOD Modules" shape="rect">Table&nbsp;A.2-1</a> specifies the Modules of the CR Image IOD.</p>
                  <div class="table">
                     <a id="table_A.2-1" shape="rect"></a>
                     <p class="title">
                        <strong>Table&nbsp;A.2-1.&nbsp;CR Image IOD Modules</strong>
                     </p>
                     <div class="table-contents">
                        <table frame="box" rules="all">
                           <thead>
                              <tr valign="top">
                                 <th align="center" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_28e42d61-377f-4682-9d88-da5e5365a395" shape="rect"></a>IE</p>
                                 </th>
                                 <th align="center" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_95fae2e4-1ed9-4d29-bc9c-0f8686e77b0b" shape="rect"></a>Module</p>
                                 </th>
                                 <th align="center" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_2ba6d8f0-4d9b-47e4-8526-d71dd7f54845" shape="rect"></a>Reference</p>
                                 </th>
                                 <th align="center" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_eca4d531-84f7-4e84-9160-0944cff46991" shape="rect"></a>Usage</p>
                                 </th>
                              </tr>
                           </thead>
                           <tbody>
                              <tr valign="top">
                                 <td align="left" rowspan="2" colspan="1">
                                    <p>
                                       <a id="para_5aa8b3f7-568e-412b-9b86-87014069f3a3" shape="rect"></a>Patient</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_bc79bc38-fded-4e83-b6cf-358317aeb7a2" shape="rect"></a>Patient</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_a3b139fa-41a0-4df8-808c-38cb364c850d" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.1" title="C.7.1.1 Patient Module" shape="rect">C.7.1.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_cf0b8a2b-c59e-407e-a1c0-45924a108d74" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_834fae3d-253a-4360-9a6f-94aee097dc49" shape="rect"></a>Clinical Trial Subject</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_41e4a5af-fc11-45db-b9ad-fe28652cc651" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.3" title="C.7.1.3 Clinical Trial Subject Module" shape="rect">C.7.1.3</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_28527800-853e-4f79-97f1-6234eb1d3c0d" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="3" colspan="1">
                                    <p>
                                       <a id="para_ef4f5872-b6f4-46a5-aabc-054a5a67e93f" shape="rect"></a>Study</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_3afefb6d-8eb6-4cf9-92fa-c6cb50873da8" shape="rect"></a>General Study</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_64574519-b874-4628-8258-5476c306da79" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.2.1" title="C.7.2.1 General Study Module" shape="rect">C.7.2.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_c5849c80-b002-43e0-ae0f-527e322e694c" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_393f2483-ba32-4664-ab6c-30c0392cc918" shape="rect"></a>Patient Study</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_7686a9ed-8ace-4b85-a6eb-72a2815beb39" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.2.2" title="C.7.2.2 Patient Study Module" shape="rect">C.7.2.2</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_7c6fc16b-6b27-4eb3-9fa4-584ab0eeb810" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_c00649d9-1926-4bd8-8605-90e358146f75" shape="rect"></a>Clinical Trial Study</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_a7033261-8521-481f-9dca-87c89c6138be" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.2.3" title="C.7.2.3 Clinical Trial Study Module" shape="rect">C.7.2.3</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_581a54f2-7e7f-4617-8cfd-0008fd799c7f" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="3" colspan="1">
                                    <p>
                                       <a id="para_e2608dce-e9da-4dd6-8940-04ea47d51a17" shape="rect"></a>Series</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_17e3d9a6-d0c7-4756-9582-1eb16888a744" shape="rect"></a>General Series</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_93be873b-e198-451c-9def-ecdccb4d8852" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.3.1" title="C.7.3.1 General Series Module" shape="rect">C.7.3.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_4cb50869-5884-4518-96d0-815ef2899275" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_7e390a4d-c5fd-46f1-8e83-79fc72edc07e" shape="rect"></a>CR Series</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_40f9906f-2965-4c48-b765-2c3b89d84a15" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.8.1.1" title="C.8.1.1 CR Series Module" shape="rect">C.8.1.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_69924ade-cc99-4d38-84cd-5f9061b498fe" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_f74f3bf3-db94-431e-987c-421ca1743d8a" shape="rect"></a>Clinical Trial Series</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_d31a6b8c-47d5-4997-bfaf-9a7f4b79b708" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.3.2" title="C.7.3.2 Clinical Trial Series Module" shape="rect">C.7.3.2</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_a2000d71-50ad-4876-a76e-d891fc4ae476" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_7371a85d-a1cd-48fd-a1d9-3efc8ef5da2d" shape="rect"></a>Equipment</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_02a38e1d-d322-4686-9342-039323a86f6d" shape="rect"></a>General Equipment</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_cf5652f6-095d-42d8-9666-a34801035ea3" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.5.1" title="C.7.5.1 General Equipment Module" shape="rect">C.7.5.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_a9a1f855-6c61-4621-ab68-358c66d0f85f" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="12" colspan="1">
                                    <p>
                                       <a id="para_55790433-b9e7-4895-b142-8a099909d824" shape="rect"></a>Image</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_5909a777-a45b-4d16-a16f-6c41a5ac1749" shape="rect"></a>General Image</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_c4f433f0-0a10-4fda-84ce-dda21638de66" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.6.1" title="C.7.6.1 General Image Module" shape="rect">C.7.6.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_b550ee7d-3988-4fe9-96a4-a5330c30e5fc" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_5fa7ace6-ca0e-4c83-8612-4b97cdf3dcb5" shape="rect"></a>Image Pixel</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_902e736f-769d-430d-9f99-0e51e4032cca" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.6.3" title="C.7.6.3 Image Pixel Module" shape="rect">C.7.6.3</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_67ef5f83-5ab2-4f7b-ad7b-6ce866b8d310" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_2d287a91-b1fd-4915-81d6-c6d8001a6d8e" shape="rect"></a>Contrast/Bolus</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_0c6dc198-fee8-4904-843c-c41e27a6e27f" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.6.4" title="C.7.6.4 Contrast/Bolus Module" shape="rect">C.7.6.4</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_941c1f1e-49cb-44ef-8b7d-5763953ab041" shape="rect"></a>C - Required if contrast media was used in this image</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_051d483d-1cef-4f58-b728-5186848916ae" shape="rect"></a>Display Shutter</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_9597d767-a5af-43e7-a302-ab76bfa0cc36" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.6.11" title="C.7.6.11 Display Shutter Module" shape="rect">C.7.6.11</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_1f78cc34-f31b-4d2f-8a21-6ceb710fed62" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_9e7645e3-a0cc-4d61-ae20-1da01ffe6e31" shape="rect"></a>Device</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_c6b37cc1-ae01-4b53-88c4-959c267d9733" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.6.12" title="C.7.6.12 Device Module" shape="rect">C.7.6.12</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_feb3027e-505b-4e9c-84e7-09c7df6d09e0" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_f0e92fe2-8733-4658-9126-852b167b4089" shape="rect"></a>Specimen</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_4a5152e5-648d-429f-a7b2-d6ab8caeed2b" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.6.22" title="C.7.6.22 Specimen Module" shape="rect">C.7.6.22</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_79ef4fa1-20ef-481b-af08-aa76769c6ae1" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_207abe81-d5ba-4695-8b18-1c92a70f3cc5" shape="rect"></a>CR Image</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_99c06c36-495a-4881-8e10-e2beb8bb5fb0" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.8.1.2" title="C.8.1.2 CR Image Module" shape="rect">C.8.1.2</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_bcc647a1-d93f-4c53-96ca-a37ac86986d7" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_d564e827-8274-47d3-b641-933aa4e9f2f9" shape="rect"></a>Overlay Plane</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_ebbdf045-b753-4245-b450-b034c19a6d4f" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.9.2" title="C.9.2 Overlay Plane Module" shape="rect">C.9.2</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_27336772-bccc-4c52-8f35-01c88d9fbec4" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_09e8b2e3-f555-40f9-85b5-98909e2e9249" shape="rect"></a>Modality LUT</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_8985bee5-74ca-417a-8eba-9d081ac04e94" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.11.1" title="C.11.1 Modality LUT Module" shape="rect">C.11.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_c2a2d701-acd7-4ff8-8931-fc6e76e9709a" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_b33b14c6-87ae-479f-908a-eaf0884be908" shape="rect"></a>VOI LUT</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_124fe9c3-fde2-46fd-8633-b8c7eb4c311a" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.11.2" title="C.11.2 VOI LUT Module" shape="rect">C.11.2</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_30157c90-d1ca-40d7-94fd-7b6208c73e56" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_522a9b46-2fc2-4482-b248-c43fe2208257" shape="rect"></a>SOP Common</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_cd8bc6b8-9d2e-4ef5-8b30-7d9c13d93ac5" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.12.1" title="C.12.1 SOP Common Module" shape="rect">C.12.1</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_5f04022b-47a0-4930-b094-c11a74283b9e" shape="rect"></a>M</p>
                                 </td>
                              </tr>
                              <tr valign="top">
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_d015b873-dcd2-44f7-bb47-51903f0f3c55" shape="rect"></a>Common Instance Reference</p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_1d02db6b-46a7-4b07-8126-ea4bf4f555c9" shape="rect"></a>
                                       <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.12.2" title="C.12.2 Common Instance Reference Module" shape="rect">C.12.2</a>
                                    </p>
                                 </td>
                                 <td align="left" rowspan="1" colspan="1">
                                    <p>
                                       <a id="para_68e1e0b5-a959-452d-9a31-8b4a09abf60a" shape="rect"></a>U</p>
                                 </td>
                              </tr>
                           </tbody>
                        </table>
                     </div>
                  </div>
                  <br class="table-break" clear="none">
                  <div class="note" style="margin-left: 0.5in; margin-right: 0.5in;">
                     <h3 class="title">Note</h3>
                     <p>
                        <a id="para_dfdad0c6-73c1-4872-9b23-f7b9fd7b59b7" shape="rect"></a>The <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.10.2" title="C.10.2 Curve Module (Retired)" shape="rect">Curve Module (Retired)</a> was previously included in the Image IE for this IOD but has been retired. See <a class="link" href="ftp://medical.nema.org/MEDICAL/Dicom/2004/printed/04_03pu3.pdf" target="_top" shape="rect">PS3.3-2004</a>.</p>
                  </div>
               </div>
            </div>

'''

patient_group_macro = '''

 <div class="table">
    <a id="table_C.7.1.4-1" shape="rect"></a>
    <p class="title">
       <strong>Table&nbsp;C.7.1.4-1.&nbsp;Patient Group Macro Attributes</strong>
    </p>
    <div class="table-contents">
       <table frame="box" rules="all">
          <thead>
             <tr valign="top">
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_f0634cf7-b29a-45a0-b884-bdf3915f87b6" shape="rect"></a>Attribute Name</p>
                </th>
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_b1993d7a-f427-4b98-bb26-2a15d8b3e8df" shape="rect"></a>Tag</p>
                </th>
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_24f3ff37-c38f-4624-bf40-94c988415514" shape="rect"></a>Type</p>
                </th>
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_b50b0311-6cad-4063-b5b4-b0c962181fa5" shape="rect"></a>Attribute Description</p>
                </th>
             </tr>
          </thead>
          <tbody>
             <tr valign="top">
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_ac463e7a-7a49-4df0-9563-925879fa192f" shape="rect"></a>Source Patient Group Identification Sequence</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_7ce8eb67-9a3b-4ebd-ad49-c72328c32afc" shape="rect"></a>(0010,0026)</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_8e67145a-175e-40d8-a2f1-c40eeb40b42a" shape="rect"></a>3</p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_4c308fd9-cd58-435d-9711-b10624077265" shape="rect"></a>A sequence containing the value used for Patient ID (0010,0020) and related Attributes in the source composite instances that contained a group of subjects whose data was acquired at the same time, from which this composite instance was extracted. See <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.4.1.1" title="C.7.1.4.1.1 Groups of Subjects" shape="rect">Section&nbsp;C.7.1.4.1.1</a>.</p>
                   <p>
                      <a id="para_131b838f-b085-4807-9cd0-724b1bb4401d" shape="rect"></a>Only a single Item is permitted in this sequence.</p>
                </td>
             </tr>
             <tr valign="top">
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_4e2c78f4-121c-446d-b4f9-00922e4b2116" shape="rect"></a>&gt;Patient ID</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_020d0ae6-aec6-474e-978c-c8e6b790e01d" shape="rect"></a>(0010,0020)</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_43bce51e-b255-44cf-9a18-291f5b02e0fa" shape="rect"></a>1</p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_86b92af1-ebec-45dc-8d5b-02d425c1e14e" shape="rect"></a>Primary identifier for the group of subjects.</p>
                </td>
             </tr>
             <tr valign="top">
                <td align="left" colspan="3" rowspan="1">
                   <p>
                      <a id="para_176f5141-c45d-44f1-8195-fc9dd6317035" shape="rect"></a>
                      <span class="italic">&gt;Include <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_10-18" title="Table 10-18. Issuer of Patient ID Macro Attributes" shape="rect">Table&nbsp;10-18 “Issuer of Patient ID Macro Attributes”</a>
                      </span>
                   </p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_a4b4d4e1-389d-4ddc-8984-163b0ad35f16" shape="rect"></a>
                   </p>
                </td>
             </tr>
             <tr valign="top">
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_b208469e-5d8c-46a2-9cf0-341bbf126814" shape="rect"></a>Group of Patients Identification Sequence</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_bf33eb29-9d28-4ac4-a046-9170a82d8795" shape="rect"></a> (0010,0027) </p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_f973bdfd-c14d-4dcf-8110-dc7622e41c1b" shape="rect"></a>
3 </p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_1b7939c6-bab7-4d07-a892-163d0f084837" shape="rect"></a>A sequence containing the identifiers and locations of the individual subjects whose data was acquired at the same time (as a group) and encoded in this composite instance. See <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.4.1.1" title="C.7.1.4.1.1 Groups of Subjects" shape="rect">Section&nbsp;C.7.1.4.1.1</a>.</p>
                   <p>
                      <a id="para_de1a0650-3c6b-4e92-99cc-d6de41bdc986" shape="rect"></a>One or more Items are permitted in this sequence.</p>
                </td>
             </tr>
             <tr valign="top">
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_647e5ca7-b0e0-4284-a4bd-240186b63810" shape="rect"></a>&gt;Patient ID</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_cfb3c2db-bc63-47c9-83b8-77c6c7893d96" shape="rect"></a>(0010,0020)</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_ce905dab-1a45-4aa3-80c3-e481dbb144e0" shape="rect"></a>1</p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_12abde71-9393-4f1a-8b60-28200e39fc8a" shape="rect"></a>Primary identifier for an individual subject.</p>
                </td>
             </tr>
             <tr valign="top">
                <td align="left" colspan="3" rowspan="1">
                   <p>
                      <a id="para_53ced2c3-7a7e-4c9e-b372-2da23c48cb40" shape="rect"></a>
                      <span class="italic">&gt;Include <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_10-18" title="Table 10-18. Issuer of Patient ID Macro Attributes" shape="rect">Table&nbsp;10-18 “Issuer of Patient ID Macro Attributes”</a>
                      </span>
                   </p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_1e78f488-9bb3-42cd-b4e0-1a107cef2a36" shape="rect"></a>
                   </p>
                </td>
             </tr>
             <tr valign="top">
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_b5abdd92-26c3-4db9-b909-fbf4d02602ff" shape="rect"></a>&gt;Subject Relative Position in Image</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_9df9cc40-9b61-4f75-9730-0728ca60a94e" shape="rect"></a>(0010,0028)</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_54be252d-c12d-4ea5-9cbe-cfbde97c5707" shape="rect"></a>3</p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_d12ecf33-092b-41b5-93c1-b808a92362e1" shape="rect"></a>The position in the image pixel data of the individual subject identified in this sequence relative to the other subjects. See <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.4.1.1.1" title="C.7.1.4.1.1.1 Subject Relative Position in Image and Patient Position" shape="rect">Section&nbsp;C.7.1.4.1.1.1</a>.</p>
                </td>
             </tr>
             <tr valign="top">
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_2f1fbbb0-5079-4c82-945d-8f5f3f00c749" shape="rect"></a>&gt;Patient Position</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_fd9d7137-5ae6-43eb-94a2-003ce45d1c37" shape="rect"></a>(0018,5100)</p>
                </td>
                <td align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_61df4667-e47e-4c9b-800a-404bc80c45eb" shape="rect"></a>3</p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_f4dcf837-531d-46af-9a64-6ae7c7a79501" shape="rect"></a>Patient position descriptor relative to the equipment.  See <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.4.1.1.1" title="C.7.1.4.1.1.1 Subject Relative Position in Image and Patient Position" shape="rect">Section&nbsp;C.7.1.4.1.1.1</a>.</p>
                   <p>
                      <a id="para_55f962dc-3a58-4e4e-b225-35388c607643" shape="rect"></a>See <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.3.1.1.2" title="C.7.3.1.1.2 Patient Position" shape="rect">Section&nbsp;C.7.3.1.1.2</a> for Defined Terms and further explanation.</p>
                </td>
             </tr>
          </tbody>
       </table>
    </div>
 </div>
 '''

macro_expand_caller = '''

 <div class="table">
    <a id="table_C.7-1" shape="rect"></a>
    <p class="title">
       <strong>Table&nbsp;C.7-1.&nbsp;Patient Module Attributes</strong>
    </p>
    <div class="table-contents">
       <table frame="box" rules="all">
          <thead>
             <tr valign="top">
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_b3c32db2-8602-4023-89bb-3856b3c51c8e" shape="rect"></a>Attribute Name</p>
                </th>
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_2f7d731b-1fef-4474-81fb-bd2eb47efb40" shape="rect"></a>Tag</p>
                </th>
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_8d036e51-8ab1-43d3-8460-77d97c7a5ff9" shape="rect"></a>Type</p>
                </th>
                <th align="center" rowspan="1" colspan="1">
                   <p>
                      <a id="para_53c874ba-0179-437b-86d0-406e872b2065" shape="rect"></a>Attribute Description</p>
                </th>
             </tr>
          </thead>
          <tbody>
             <tr valign="top">
                <td align="left" colspan="3" rowspan="1">
                   <p>
                      <a id="para_066d6894-dcf3-476c-a67d-d59366cb430d" shape="rect"></a>
                      <span class="italic">Include <a class="xref" href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7.1.4-1" title="Table C.7.1.4-1. Patient Group Macro Attributes" shape="rect">Table&nbsp;C.7.1.4-1 “Patient Group Macro Attributes”</a>
                      </span>
                   </p>
                </td>
                <td align="left" rowspan="1" colspan="1">
                   <p>
                      <a id="para_a9ef0519-e45f-498b-82c4-d9980afde268" shape="rect"></a>
                   </p>
                </td>
             </tr>
          </tbody>
       </table>
    </div>
 </div>
'''

properties_snippet = '''
<div class="table">
   <a id="table_6-1" shape="rect"></a>
   <p class="title">
      <strong>Table 6-1. Registry of DICOM Data Elements</strong>
   </p>
   <div class="table-contents">
      <table frame="box" rules="all">
         <thead>
            <tr valign="top">
               <th align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_3e8c52d5-3582-4ec4-a7e6-acd7604caf32" shape="rect"></a>
                     <span class="bold">
                        <strong>Tag</strong>
                     </span>
                  </p>
               </th>
               <th align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_ac298c3b-bcdd-462b-9240-c38e738bfb7c" shape="rect"></a>
                     <span class="bold">
                        <strong>Name</strong>
                     </span>
                  </p>
               </th>
               <th align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_99f6b0ff-e1b0-484e-83b5-c3003d61704c" shape="rect"></a>
                     <span class="bold">
                        <strong>Keyword</strong>
                     </span>
                  </p>
               </th>
               <th align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_42b3621d-8b30-46eb-8992-10bb21310ac7" shape="rect"></a>
                     <span class="bold">
                        <strong>VR</strong>
                     </span>
                  </p>
               </th>
               <th align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_551ea829-a949-4bfd-a201-bb102024e64c" shape="rect"></a>
                     <span class="bold">
                        <strong>VM</strong>
                     </span>
                  </p>
               </th>
               <th align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_3a18713f-2e81-4664-b9a1-e4e3d41957ab" shape="rect"></a>
                  </p>
               </th>
            </tr>
         </thead>
         <tbody>
            <tr valign="top">
               <td align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_a3b3bd4c-066d-47ca-9cfc-310e017063df" shape="rect"></a>
                     <span class="italic">(0008,0001)</span>
                  </p>
               </td>
               <td align="left" rowspan="1" colspan="1">
                  <p>
                     <a id="para_98dadd68-a5fc-4f46-9590-cf129f76a96f" shape="rect"></a>
                     <span class="italic">Length to End</span>
                  </p>
               </td>
               <td align="left" rowspan="1" colspan="1">
                  <p>
                     <a id="para_d4f02df2-6cdf-4324-afb8-5d033d1d63a2" shape="rect"></a>
                     <span class="italic">Length ToEnd</span>
                  </p>
               </td>
               <td align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_40ad40bf-10cb-42fe-bf58-10794de1d4e7" shape="rect"></a>
                     <span class="italic">UL</span>
                  </p>
               </td>
               <td align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_f0c1b432-1911-4196-ac5e-c50217908dd9" shape="rect"></a>
                     <span class="italic">1</span>
                  </p>
               </td>
               <td align="center" rowspan="1" colspan="1">
                  <p>
                     <a id="para_b8e51f4b-5e85-4337-b2a7-14eecec3d1f5" shape="rect"></a>
                     <span class="italic">RET</span>
                  </p>
               </td>
            </tr>
        </tbody>
        </table>
    </div>
</div>
'''
