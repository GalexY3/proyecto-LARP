/* R01 — source-frozen non-redistributive geometry QA for nine real HSI sparse point tables.
 * Ordinary CSV numeric columns only. No MHU, LOCAL, CVT, Wei algorithm executed here.
 */
function auditR01(filedict) {
  'use strict';
  const ids=['1722','1723','1724','1725','1726','1727','1728','1729','1730'];
  const hashes={
    '1722':'b5ab7469b273213cbf800870738f6e73a708287e',
    '1723':'74c1026341b8c28d9fbb168127e89b233e28c8e',
    '1724':'ea8e7b0e65e68218b2c4fcb307438955f4d08c7c',
    '1725':'d965d15025ac1594952b1620fed5627ab46de2f7',
    '1726':'877d9cf02fbfad9f98eb6cdf21c066c26820f10c',
    '1727':'864a65a5960435227dcfb9d033089cde15062842',
    '1728':'5802465683f2616c87eaa9c6ef3819d787328107',
    '1729':'15ce357543777fdd9a50b0a6723a6bd19f3c840b',
    '1730':'bfb836529be7958476353093085677f629d95f7'
  };
  if(Object.keys(filedict).length!==9||ids.some(id=>!filedict[id]||typeof filedict[id].content!=='string'||filedict[id].blob!==hashes[id]))throw Error('SOURCE_SHA_OR_SCENE_SET_MISMATCH');
  const median=x=>{if(!x.length)return null;const a=x.slice().sort((b,c)=>b-c),m=Math.floor(a.length/2);return a.length%2?a[m]:(a[m-1]+a[m])/2;};
  const out=[];
  for(const id of ids) {
    const lines=filedict[id].content.trim().split(/\r?\n/),head=lines[0].split(',');
    const target=['ID','X','Y',...Array.from({length:204},(_,i)=>'Band_'+(i+1))];
    if(head.length!==target.length||head.some((s,i)=>s!==target[i]))throw Error('SCHEMA_MISMATCH_'+id);
    let malformed=0,nonfiniteRows=0,bandNegative=0,bandAboveOne=0,bandCells=0,duplicateIds=0,duplicateXY=0,badCoordinate=0;
    const pts=[],seenCoord=new Set(),seenId=new Set();
    for(let i=1;i<lines.length;i++){
      const z=lines[i].split(',');
      if(z.length!==207){malformed++;continue;}
      const nums=z.map(Number),x=nums[1],y=nums[2];
      if(!nums.every(Number.isFinite)){nonfiniteRows++;continue;}
      const intCoords=Number.isInteger(x)&&Number.isInteger(y)&&x>=1&&y>=1;
      if(!intCoords)badCoordinate++;
      if(seenId.has(nums[0]))duplicateIds++;seenId.add(nums[0]);
      const k=x+'_'+y;if(seenCoord.has(k))duplicateXY++;seenCoord.add(k);
      const bands=nums.slice(3);
      bandCells+=bands.length;for(const v of bands){if(v<0)bandNegative++;if(v>1)bandAboveOne++;}
      pts.push({x,y});
    }
    const xs=pts.map(p=>p.x),ys=pts.map(p=>p.y);
    const xrange=pts.length?[Math.min(...xs),Math.max(...xs)]:null,yrange=pts.length?[Math.min(...ys),Math.max(...ys)]:null;
    const bboxArea=pts.length&&(xrange[1]>=xrange[0])&&(yrange[1]>=yrange[0])?(xrange[1]-xrange[0]+1)*(yrange[1]-yrange[0]+1):null;
    const nn=pts.length>=2?pts.map((p,i)=>Math.min(...pts.filter((_,j)=>j!==i).map(q=>Math.hypot(p.x-q.x,p.y-q.y)))):[];
    const nondegenerate=pts.length>=3&&xrange[0]<xrange[1]&&yrange[0]<yrange[1];
    const eligible=pts.length>=400&&duplicateXY===0&&malformed===0&&nonfiniteRows===0&&badCoordinate===0&&nondegenerate;
    out.push({
      scene_id:id,git_blob:hashes[id],bands:204,physical_source:'REPORTED_2D_IMAGE_EXTRACTED_CENTROIDS',
      raw_data_lines:lines.length-1,valid_finite_points:pts.length,malformed,nonfiniteRows,duplicateIds,duplicateXY,badCoordinate,
      x_range:xrange,y_range:yrange,bbox_area_pixels:bboxArea,observed_occupancy_within_bbox:pts.length&&bboxArea?seenCoord.size/bboxArea:null,
      median_nearest_sample_distance_pixels:median(nn),bands_checked_cells:bandCells,negative_band_values:bandNegative,above_one_band_values:bandAboveOne,
      eligible_for_original_N400_with_400_unique_observed_pixels:eligible
    });
  }
  const nEligible=out.filter(s=>s.eligible_for_original_N400_with_400_unique_observed_pixels).length;
  return {
    protocol:'R01_HSI_SPARSE_GEOMETRY_QA',upstream_repo:'szkymm/Gra_Desi',upstream_commit:'8157f619f11bef20564067d55450c53120d1a712',
    upstream_license_scope:'README_ASSERTS_GPL3_FOR_PROJECT_BUT_RAW_SPECTRAL_DATA_RIGHTS_NOT_CONFIRMED',
    coordinate_origin:'image_tag.py: HSV green segmentation + contour centroid, then obtain_reflectance.py extracts values from original image at those selected centers',
    scenes:out,totals:{scenes:out.length,valid_finite_points:out.reduce((n,r)=>n+r.valid_finite_points,0),scenes_with_400_unique_observed_pixels:nEligible,
      passed_original_N400_parity_gate:nEligible>=3,scenes_204bands:out.filter(s=>s.bands===204).length,
      all_scene_ids_checked:out.map(s=>s.scene_id)},
    evidence_boundary:['NOT_FULL_2D_HSI_CUBE','NON_RANDOM_CONTOUR_SELECTED_POINTS','NO_ORIGINAL_WEI_RUN','NO_MHU_LOCAL_CVT_GEOMETRY_COMPARE','NO_RAW_SPECTRAL_DATA_REPUBLISHED'],
    recommendation:nEligible>=3?'EXAMINE_MANUAL_GEOMETRY_BIAS_AND_WEI_BINARY_FIRST':'STOP_HSI_SPARSE_FOR_N400_PARITY',
    grade:'0/3',CT2_math_before_after:[24,24],CT2_functional_before_after:[18,18]
  };
}