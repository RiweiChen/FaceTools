Path='H:\Dataset\MyDatasets\Face_Expression_Pair\CAS_PEAL';
dirlist=dir(Path);
lendir=size(dirlist,1);
fid=fopen('imagelist_caspeal.txt', 'w');
for i=3:lendir
%     dirlist(i).name
    file1=[Path '\' dirlist(i).name '\0.jpg'];
    fprintf(fid,'%s\r\n',file1);
    file2=[Path '\' dirlist(i).name '\1.jpg'];
    fprintf(fid,'%s\r\n',file2);
end
fclose(fid);